from django.shortcuts import render, redirect
from django.views.generic import View
from .models import Batches
from .forms import BatchRegisterForm

# Create your views here.

from .models import Batches
from django.utils.decorators import method_decorator

from authentication.permissions import permission_roles

class GetBatchObject:

    def get_batch(self, request, uuid):

        try:

            batch = Batches.objects.get(uuid=uuid)

            return batch

        except Batches.DoesNotExist:

            return render(request, "errorpages/error-404.html")
class BatchesView(View):
    def get(self, request):
        batches = Batches.objects.all()
        return render(request, "batches/batches_list.html", {"batches": batches})


class AddBatchesView(View):
    def get(self, request):
        form = BatchRegisterForm()
        return render(request, "batches/add_batches.html", {"form": form})

    def post(self, request):
        form = BatchRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("batches_list")
        return render(request, "batches/add_batches.html", {"form": form})

@method_decorator(
    permission_roles(roles=["Admin", "Sales", "Trainer", "Academic Counsellor"]),
    name="dispatch",
)
class BatchDetailView(View):

    def get(self, request, *args, **kwargs):

        uuid = kwargs.get("uuid")

        try:

            batch = Batches.objects.get(uuid=uuid)

        except:

            return redirect("error-404")

        data = {"batch": batch}

        return render(request, "batches/batch-detail.html", context=data)


@method_decorator(permission_roles(roles=["Admin", "Sales"]), name="dispatch")
class BatchDeleteView(View):

    def get(self, request, *args, **kwargs):

        uuid = kwargs.get("uuid")

        try:

            batch = Batches.objects.get(uuid=uuid)

        except Batches.DoesNotExist:

            return redirect("error-404")

        # batch.delete()

        batch.active_status = False

        batch.save()

        return redirect("batches_list")


@method_decorator(permission_roles(roles=["Admin", "Sales"]), name="dispatch")
class BatchUpdateView(View):

    def get(self, request, *args, **kwargs):

        uuid = kwargs.get("uuid")

        batch = GetBatchObject().get_batch(request, uuid)

        form = BatchRegisterForm(instance=batch)

        data = {"form": form}

        return render(request, "batches/batch-update.html", context=data)

    def post(self, request, *args, **kwargs):

        uuid = kwargs.get("uuid")

        batch = GetBatchObject().get_batch(request, uuid)

        form = BatchRegisterForm(request.POST, request.FILES, instance=batch)

        if form.is_valid():

            batch.active_status = True

            form.save()

            return redirect("batch_list")

        print(form.errors)

        data = {"form": form}

        return render(request, "batches/batch-update.html", context=data)
