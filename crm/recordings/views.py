from django.views import View
from django.shortcuts import render, redirect, HttpResponse
from django.urls import reverse
from django.utils import timezone
from .forms import RecordingForm
from .models import Recording
from django.core.paginator import Paginator

class RecordingsView(View):
    def get(self, request, *args, **kwargs):
        """
        Render the recordings page.
        """
        recordings = Recording.objects.order_by("created_at")
        paginator      = Paginator(recordings, 3)  # Show 3 recordings per page
        page_number    = request.GET.get("page")                    # ?page=2
        page_obj       = paginator.get_page(page_number)
        context = {
        "page_obj": page_obj,         
        "recordings": page_obj.object_list, # List of recordings for the current page
        }
        return render(request, "recordings/recordings.html", context)

def recording_create(request):
    """Create recording — supports normal page and JS popup (window.open)."""
    is_popup = request.GET.get("popup") or request.POST.get("popup")
    referer = request.META.get("HTTP_REFERER") or reverse("recording-list")

    if request.method == "POST":
        form = RecordingForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('recordings') 
    else:
        form = RecordingForm()

    ctx = {"form": form, "referer": referer, "is_popup": is_popup}
    return render(request, "recordings/add-video.html", ctx)