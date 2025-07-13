# courses/views.py
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import CreateView, ListView
from .models import Courses
from .forms import CourseForm
from django.urls import reverse


class CourseListView(ListView):
    def get(self, request, *args, **kwargs):
        courses = Courses.objects.all().order_by("-created_at")
        paginator = Paginator(courses, 1)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        context = {
            "page_obj": page_obj,
            "courses": page_obj.object_list,  # List of courses for the current page
        }
        return render(request, "courses/course_list.html", context)

def course_create(request):
    is_popup = request.GET.get("popup") or request.POST.get("popup")
    referer = request.META.get("HTTP_REFERER") or reverse("recording-list")

    if request.method == "POST":
        form = CourseForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('course-list') 
    else:
        form = CourseForm()

    ctx = {"form": form, "referer": referer, "is_popup": is_popup}
    return render(request, "courses/course_form.html", ctx)
