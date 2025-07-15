# batches/forms.py
from django import forms
from django.core.exceptions import ValidationError
from batches.models import Batches
from courses.models import Courses
from trainers.models import Trainers
from academic_counsellors.models import AcademicCounsellor


class BatchRegisterForm(forms.ModelForm):
    # Tailwind: red ring on invalid fields automatically
    error_css_class = "border-red-500 ring-1 ring-red-500"

    # ────────── Foreign‑key dropdowns ──────────
    academic_counsellor = forms.ModelChoiceField(
        queryset=AcademicCounsellor.objects.all(),
        empty_label="Select Academic Counsellor",
        error_messages={"required": "Please choose an academic counsellor."},
        widget=forms.Select(
            attrs={
                "class": "block w-full mt-1 text-sm dark:text-gray-300 dark:border-gray-600 "
                "dark:bg-gray-700 form-select focus:border-purple-400 focus:outline-none "
                "focus:shadow-outline-purple dark:focus:shadow-outline-gray",
                "required": "required",
            }
        ),
    )

    courses = forms.ModelChoiceField(  # ← singular, matches model field
        queryset=Courses.objects.all(),
        empty_label="Select Course",
        error_messages={"required": "Please choose a course."},
        widget=forms.Select(
            attrs={
                "class": "block w-full mt-1 text-sm dark:text-gray-300 dark:border-gray-600 "
                "dark:bg-gray-700 form-select focus:border-purple-400 focus:outline-none "
                "focus:shadow-outline-purple dark:focus:shadow-outline-gray",
                "required": "required",
            }
        ),
    )

    trainer = forms.ModelChoiceField(
        queryset=Trainers.objects.all(),
        empty_label="Select Trainer",
        error_messages={"required": "Please choose a trainer."},
        widget=forms.Select(
            attrs={
                "class": "block w-full mt-1 text-sm dark:text-gray-300 dark:border-gray-600 "
                "dark:bg-gray-700 form-select focus:border-purple-400 focus:outline-none "
                "focus:shadow-outline-purple dark:focus:shadow-outline-gray",
                "required": "required",
            }
        ),
    )

    # ────────── Meta section ──────────
    class Meta:
        model = Batches
        # exclude non‑editable / auto fields
        exclude = [
            "batch_ended",
            "ended_on",
            "uuid",
            "active_status",
        ]  # adjust field names as in your model

        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "block w-full mt-1 text-sm dark:border-gray-600 dark:bg-gray-700 "
                    "focus:border-purple-400 focus:outline-none focus:shadow-outline-purple "
                    "dark:text-gray-300 dark:focus:shadow-outline-gray form-input",
                    "required": "required",
                }
            ),
            "start_date": forms.DateInput(
                attrs={
                    "type": "date",
                    "class": "block w-full mt-1 text-sm dark:border-gray-600 dark:bg-gray-700 "
                    "focus:border-purple-400 focus:outline-none focus:shadow-outline-purple "
                    "dark:text-gray-300 dark:focus:shadow-outline-gray form-input",
                    "required": "required",
                }
            ),
            "expecting_end_date": forms.DateInput(
                attrs={
                    "type": "date",
                    "class": "block w-full mt-1 text-sm dark:border-gray-600 dark:bg-gray-700 "
                    "focus:border-purple-400 focus:outline-none focus:shadow-outline-purple "
                    "dark:text-gray-300 dark:focus:shadow-outline-gray form-input",
                    "required": "required",
                }
            ),
            "offline_capacity": forms.NumberInput(
                attrs={
                    "min": 1,
                    "class": "block w-full mt-1 text-sm dark:border-gray-600 dark:bg-gray-700 "
                    "focus:border-purple-400 focus:outline-none focus:shadow-outline-purple "
                    "dark:text-gray-300 dark:focus:shadow-outline-gray form-input",
                    "required": "required",
                }
            ),
            "online_capacity": forms.NumberInput(
                attrs={
                    "min": 1,
                    "class": "block w-full mt-1 text-sm dark:border-gray-600 dark:bg-gray-700 "
                    "focus:border-purple-400 focus:outline-none focus:shadow-outline-purple "
                    "dark:text-gray-300 dark:focus:shadow-outline-gray form-input",
                    "required": "required",
                }
            ),
        }

    # ────────── Form‑wide validation ──────────
    def clean(self):
        cleaned = super().clean()

        start = cleaned.get("start_date")
        end = cleaned.get("expecting_end_date")
        off = cleaned.get("offline_capacity")
        onl = cleaned.get("online_capacity")

        # End date must come after start date
        if start and end and end <= start:
            self.add_error(
                "expecting_end_date",
                "Expecting end date must be after the start date.",
            )

        # Capacities must be positive numbers
        if off is not None and off <= 0:
            self.add_error(
                "offline_capacity", "Offline capacity must be greater than zero."
            )

        if onl is not None and onl <= 0:
            self.add_error(
                "online_capacity", "Online capacity must be greater than zero."
            )

        return cleaned

    # ────────── Optional: one‑off tweaks on init ──────────
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Example: disable course change when editing an existing batch
        if self.instance and self.instance.pk:
            self.fields["courses"].disabled = True
