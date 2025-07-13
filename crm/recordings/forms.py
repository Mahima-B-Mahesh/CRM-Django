from django import forms
from .models import Recording

class RecordingForm(forms.ModelForm):
    class Meta:
        model = Recording
        fields = ["youtube_url", "title", "description"]
        widgets = {
            "youtube_url": forms.URLInput(attrs={
                "class": "w-full px-4 py-2 border rounded-lg",
                "placeholder": "Paste YouTube URL",
                "id": "id_youtube_url",
                "required": True,
            }),
            "title": forms.TextInput(attrs={
                "class": "w-full px-4 py-2 border rounded-lg",
                "placeholder": "Add a title",
            }),
            "description": forms.Textarea(attrs={
                "class": "w-full px-4 py-2 border rounded-lg",
                "placeholder": "Short description (optional)",
                "rows": 3,
            }),
        }