from django.shortcuts import render, redirect

# Create your views here.
from django.views import View

# from .models import DistrictChoices,CourseChoices,BatchChoices,TrainerChoices

from .utility import get_admission_number, get_password, send_email

from .models import Students

from .forms import StudentRegisterForm

from django.db.models import Q

from authentication.models import Profile

from django.db import transaction

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from authentication.permissions import permission_roles


from django.contrib import messages

from django.conf import settings

import threading

import datetime

#payments related imports
from Payments.models import Payments

class GetStudentObject:

    def get_student(self, request, uuid):

        try:

            student = Students.objects.get(uuid=uuid)

            return student

        except Students.DoesNotExist:

            return render(request, "errorpages/error-404.html")


@method_decorator(permission_roles(roles=["Admin", "Sales"]), name="dispatch")
class DashboardView(View):

    def get(self, request, *args, **kwargs):

        return render(request, "students/dashboard.html")


@method_decorator(
    permission_roles(roles=["Admin", "Sales", "Trainer", "Academic Councellor"]),
    name="dispatch",
)
class StudentsListView(View):

    def get(self, request, *args, **kwargs):

        # students = Students.objects.all()

        query = request.GET.get("query")

        role = request.user.role

        if role in ["Trainer"]:

            students = students.objects.filter(
                active_status=True, trainer__profile=request.user
            )

            if query:
                students = Students.objects.filter(
                    Q(active_status=True)
                    & Q(trainer__profile=request.user)
                    & (
                        Q(first_name__icontains=query)
                        | Q(second_name__icontains=query)
                        | Q(email__icontains=query)
                        | Q(contact__icontains=query)
                        | Q(house_name__icontains=query)
                        | Q(post_office__icontains=query)
                        | Q(district__icontains=query)
                        | Q(pincode__icontains=query)
                        | Q(adm_number__icontains=query)
                        | Q(course__name__icontains=query)
                        | Q(batch__name__icontains=query)
                        | Q(trainer__first_name__icontains=query)
                        | Q(trainer__last_name__icontains=query)
                        | Q(join_date__icontains=query)
                    )
                )
        else:
            if query:

                students = Students.objects.filter(active_status=True)

                students = Students.objects.filter(
                    Q(active_status=True)
                    & (
                        Q(first_name__icontains=query)
                        | Q(second_name__icontains=query)
                        | Q(email__icontains=query)
                        | Q(contact__icontains=query)
                        | Q(house_name__icontains=query)
                        | Q(post_office__icontains=query)
                        | Q(district__icontains=query)
                        | Q(pincode__icontains=query)
                        | Q(adm_number__icontains=query)
                        | Q(course__name__icontains=query)
                        | Q(batch__name__icontains=query)
                        | Q(trainer__first_name__icontains=query)
                        | Q(trainer__last_name__icontains=query)
                        | Q(join_date__icontains=query)
                    )
                )

        if role in ["Academic Counsellor"]:

            students = Students.objects.filter(
                active_status=True, batch__academic_counsellor__profile=request.user
            )

            if query:
                students = Students.objects.filter(
                    Q(active_status=True)
                    & Q(batch__academic_counsellor__profile=request.user)
                    & (
                        Q(first_name__icontains=query)
                        | Q(second_name__icontains=query)
                        | Q(email__icontains=query)
                        | Q(contact__icontains=query)
                        | Q(house_name__icontains=query)
                        | Q(post_office__icontains=query)
                        | Q(district__icontains=query)
                        | Q(pincode__icontains=query)
                        | Q(adm_number__icontains=query)
                        | Q(course__name__icontains=query)
                        | Q(batch__name__icontains=query)
                        | Q(trainer__first_name__icontains=query)
                        | Q(trainer__last_name__icontains=query)
                        | Q(join_date__icontains=query)
                    )
                )
        else:

            students = Students.objects.filter(active_status=True)

            if query:
                students = Students.objects.filter(
                    Q(active_status=True)
                    & (
                        Q(first_name__icontains=query)
                        | Q(second_name__icontains=query)
                        | Q(email__icontains=query)
                        | Q(contact__icontains=query)
                        | Q(house_name__icontains=query)
                        | Q(post_office__icontains=query)
                        | Q(district__icontains=query)
                        | Q(pincode__icontains=query)
                        | Q(adm_number__icontains=query)
                        | Q(course__name__icontains=query)
                        | Q(batch__name__icontains=query)
                        | Q(trainer__first_name__icontains=query)
                        | Q(trainer__last_name__icontains=query)
                        | Q(join_date__icontains=query)
                    )
                )
        data = {"students": students, "query": query}

        return render(request, "students/students.html", context=data)


@method_decorator(permission_roles(roles=["Admin", "Sales"]), name="dispatch")
class StudentRegisterView(View):

    def get(self, request, *args, **kwargs):

        form = StudentRegisterForm()

        # data = {'districts':DistrictChoices,'courses':CourseChoices,'batches':BatchChoices,'trainers':TrainerChoices,'form':form}

        data = {"form": form}

        return render(request, "students/register.html", context=data)

    def post(self, request, *args, **kwargs):

        form = StudentRegisterForm(request.POST, request.FILES)

        if form.is_valid():
            with transaction.atomic():

                student = form.save(commit=False)
                username = student.email

                password = get_password()

                print("password:", password)

                if Profile.objects.filter(username=student.email).exists():
                    messages.error(request, "A student with this email already exists.")
                    return render(
                        request, "students/register.html", context={"form": form}
                    )

                profile = Profile.objects.create_user(
                    username=username, password=password, role="Student"
                )

                student.profile = profile

                student.adm_number = get_admission_number()

                # student.join_date = '2025-02-05'

                student.active_status = True

            student.save()
            
            #payment section
            Payments.objects.create(
                student=student,
                amount=student.course.offer_fee if student.course.offer_fee else student.course.fee)
            

            subject = "Login Credentials for Student Portal"

            sender = settings.EMAIL_HOST_USER

            recepient = student.email

            template = "email/login-credentials.html"

            join_date = student.join_date

            date_after_10_days = join_date + datetime.timedelta(days=10)

            context = {
                "name": f"{student.first_name} {student.second_name}",
                "username": username,
                "password": password,
                "date_after_10_days": date_after_10_days.strftime("%Y-%m-%d"),
            }

            send_email(subject, recepient, template, context)
            thread = threading.Thread(
                target=send_email, args=(subject, recepient, template, context)
            )
            thread.start()
            return redirect("students-list")

        else:

            return render(request, "students/register.html", context={"form": form})

        # form_data = request.POST

        # first_name = form_data.get('firstname')

        # last_name = form_data.get('lastname')

        # photo = request.FILES.get('photo')

        # email = form_data.get('email')

        # contact_number = form_data.get('contact')

        # house_name = form_data.get('housename')

        # district = form_data.get('district')

        # post_office = form_data.get('postoffice')

        # pincode = form_data.get('pincode')

        # course = form_data.get('course')

        # batch = form_data.get('batch')

        # batch_date = form_data.get('batchdate')

        # trainer = form_data.get('trainer')
        # # print(first_name,last_name,photo,email,contact_number,house_name,district,post_office,pincode,course,batch,batch_date,trainer)

        # adm_number = get_admission_number()

        # join_date = '2024-08-16'

        # Students.objects.create(first_name=first_name,
        #                         second_name=last_name,
        #                         photo=photo,
        #                         email=email,
        #                         contact=contact_number,
        #                         house_name=house_name,
        #                         post_office=post_office,
        #                         district=district,
        #                         pincode=pincode,
        #                         adm_number=adm_number,
        #                         course=course,
        #                         batch=batch,
        #                         batch_date=batch_date,
        #                         join_date=join_date,
        #                         trainer_name=trainer)


@method_decorator(
    permission_roles(roles=["Admin", "Sales", "Trainer", "Academic Counsellor"]),
    name="dispatch",
)
class StudentDetailView(View):

    def get(self, request, *args, **kwargs):

        uuid = kwargs.get("uuid")

        try:

            student = Students.objects.get(uuid=uuid)

        except:

            return redirect("error-404")

        data = {"student": student}

        return render(request, "students/student-detail.html", context=data)


@method_decorator(permission_roles(roles=["Admin", "Sales"]), name="dispatch")
class StudentDeleteView(View):

    def get(self, request, *args, **kwargs):

        uuid = kwargs.get("uuid")

        try:

            student = Students.objects.get(uuid=uuid)

        except Students.DoesNotExist:

            return redirect("error-404")

        # student.delete()

        student.active_status = False

        student.save()

        return redirect("students-list")


@method_decorator(permission_roles(roles=["Admin", "Sales"]), name="dispatch")
class StudentUpdateView(View):

    def get(self, request, *args, **kwargs):

        uuid = kwargs.get("uuid")

        student = GetStudentObject().get_student(request, uuid)

        form = StudentRegisterForm(instance=student)

        data = {"form": form}

        return render(request, "students/student-update.html", context=data)

    def post(self, request, *args, **kwargs):

        uuid = kwargs.get("uuid")

        student = GetStudentObject().get_student(request, uuid)

        form = StudentRegisterForm(request.POST, request.FILES, instance=student)

        if form.is_valid():

            student.active_status = True

            form.save()

            return redirect("students-list")

        print(form.errors)

        data = {"form": form}

        return render(request, "students/student-update.html", context=data)
