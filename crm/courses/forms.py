# courses/forms.py
from django import forms
from .models import Courses

class CourseForm(forms.ModelForm):
    class Meta:
        model  = Courses
        fields = ["name", "photo", "duration", "code", "fee", "offer_fee"]
        widgets = {
            "name":      forms.TextInput(attrs={"class": "w-full px-3 py-2 border rounded required"}),
            "duration":  forms.TextInput(attrs={"class": "w-full px-3 py-2 border rounded required"}),
            "code":      forms.TextInput(attrs={"class": "w-full px-3 py-2 border rounded required"}),
            "fee":       forms.NumberInput(attrs={"class": "w-full px-3 py-2 border rounded required"}),
            "offer_fee": forms.NumberInput(attrs={"class": "w-full px-3 py-2 border rounded"}),
        }
