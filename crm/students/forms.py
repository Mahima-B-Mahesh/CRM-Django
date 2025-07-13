from django import forms

from .models import (
    Students,
    DistrictChoices,
)

from batches.models import Batches

from courses.models import Courses

from trainers.models import Trainers


class StudentRegisterForm(forms.ModelForm):

    class Meta:

        model = Students

        exclude = ["adm_number", "join_date", "uuid", "profile"]

        widgets = {
            "first_name": forms.TextInput(
                attrs={
                    "class": "block w-full mt-1 text-sm dark:border-gray-600 dark:bg-gray-700 focus:border-purple-400 focus:outline-none focus:shadow-outline-purple dark:text-gray-300 dark:focus:shadow-outline-gray form-input",
                    "required": "required",
                }
            ),
            "second_name": forms.TextInput(
                attrs={
                    "class": "block w-full mt-1 text-sm dark:border-gray-600 dark:bg-gray-700 focus:border-purple-400 focus:outline-none focus:shadow-outline-purple dark:text-gray-300 dark:focus:shadow-outline-gray form-input",
                    "required": "required",
                }
            ),
            "photo": forms.FileInput(
                attrs={
                    "class": "block w-full mt-1 text-sm dark:border-gray-600 dark:bg-gray-700 focus:border-purple-400 focus:outline-none focus:shadow-outline-purple dark:text-gray-300 dark:focus:shadow-outline-gray form-input",
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "class": "block w-full mt-1 text-sm dark:border-gray-600 dark:bg-gray-700 focus:border-purple-400 focus:outline-none focus:shadow-outline-purple dark:text-gray-300 dark:focus:shadow-outline-gray form-input",
                    "required": "required",
                }
            ),
            "contact": forms.TextInput(
                attrs={
                    "class": "block w-full mt-1 text-sm dark:border-gray-600 dark:bg-gray-700 focus:border-purple-400 focus:outline-none focus:shadow-outline-purple dark:text-gray-300 dark:focus:shadow-outline-gray form-input",
                    "required": "required",
                }
            ),
            "house_name": forms.TextInput(
                attrs={
                    "class": "block w-full mt-1 text-sm dark:border-gray-600 dark:bg-gray-700 focus:border-purple-400 focus:outline-none focus:shadow-outline-purple dark:text-gray-300 dark:focus:shadow-outline-gray form-input",
                    "required": "required",
                }
            ),
            "post_office": forms.TextInput(
                attrs={
                    "class": "block w-full mt-1 text-sm dark:border-gray-600 dark:bg-gray-700 focus:border-purple-400 focus:outline-none focus:shadow-outline-purple dark:text-gray-300 dark:focus:shadow-outline-gray form-input",
                    "required": "required",
                }
            ),
            "pincode": forms.TextInput(
                attrs={
                    "class": "block w-full mt-1 text-sm dark:border-gray-600 dark:bg-gray-700 focus:border-purple-400 focus:outline-none focus:shadow-outline-purple dark:text-gray-300 dark:focus:shadow-outline-gray form-input",
                    "required": "required",
                }
            ),
            # "batch_date": forms.DateInput(
            #     attrs={
            #         "class": "block w-full mt-1 text-sm dark:border-gray-600 dark:bg-gray-700 focus:border-purple-400 focus:outline-none focus:shadow-outline-purple dark:text-gray-300 dark:focus:shadow-outline-gray form-input",
            #         "required": "required",
            #     }
            # ),
        }

    district = forms.ChoiceField(
        choices=DistrictChoices.choices,
        widget=forms.Select(
            attrs={
                "class": "block w-full mt-1 text-sm dark:text-gray-300 dark:border-gray-600 dark:bg-gray-700 form-select focus:border-purple-400 focus:outline-none focus:shadow-outline-purple dark:focus:shadow-outline-gray",
                "required": "required",
            }
        ),
    )
    # course = forms.ChoiceField(
    #     choices=CourseChoices.choices,
    #     widget=forms.Select(
    #         attrs={
    #             "class": "block w-full mt-1 text-sm dark:text-gray-300 dark:border-gray-600 dark:bg-gray-700 form-select focus:border-purple-400 focus:outline-none focus:shadow-outline-purple dark:focus:shadow-outline-gray",
    #             "required": "required",
    #         }
    #     ),
    # )

    course = forms.ModelChoiceField(
        queryset=Courses.objects.all(),
        empty_label="Select Course",
        widget=forms.Select(
            attrs={
                "class": "block w-full mt-1 text-sm dark:text-gray-300 dark:border-gray-600 dark:bg-gray-700 form-select focus:border-purple-400 focus:outline-none focus:shadow-outline-purple dark:focus:shadow-outline-gray",
                "required": "required",
            }
        ),
    )

    # batch = forms.ChoiceField(
    #     choices=BatchChoices.choices,
    #     widget=forms.Select(
    #         attrs={
    #             "class": "block w-full mt-1 text-sm dark:text-gray-300 dark:border-gray-600 dark:bg-gray-700 form-select focus:border-purple-400 focus:outline-none focus:shadow-outline-purple dark:focus:shadow-outline-gray",
    #             "required": "required",
    #         }
    #     ),
    # )

    batch = forms.ModelChoiceField(
        queryset=Batches.objects.all(),
        empty_label="Select Batch",
        widget=forms.Select(
            attrs={
                "class": "block w-full mt-1 text-sm dark:text-gray-300 dark:border-gray-600 dark:bg-gray-700 form-select focus:border-purple-400 focus:outline-none focus:shadow-outline-purple dark:focus:shadow-outline-gray",
                "required": "required",
            }
        ),
    )

    # trainer_name = forms.ChoiceField(
    #     choices=TrainerChoices.choices,
    #     widget=forms.Select(
    #         attrs={
    #             "class": "block w-full mt-1 text-sm dark:text-gray-300 dark:border-gray-600 dark:bg-gray-700 form-select focus:border-purple-400 focus:outline-none focus:shadow-outline-purple dark:focus:shadow-outline-gray",
    #             "required": "required",
    #         }
    #     ),
    # )

    trainer = forms.ModelChoiceField(
        queryset=Trainers.objects.all(),
        empty_label="Select Trainer",
        widget=forms.Select(
            attrs={
                "class": "block w-full mt-1 text-sm dark:text-gray-300 dark:border-gray-600 dark:bg-gray-700 form-select focus:border-purple-400 focus:outline-none focus:shadow-outline-purple dark:focus:shadow-outline-gray",
                "required": "required",
            }
        ),
    )

    def clean(self):

        cleaned_data = super().clean()

        pincode = cleaned_data.get("pincode")

        email = cleaned_data.get("email")

        if pincode and (not pincode.isdigit() or len(pincode) != 6):

            self.add_error("pincode", "Pincode must be a 6-digit number")

        if email and Students.objects.filter(email=email).exists():
            self.add_error("email", "Email is already in use.")

        if Students.objects.filter(profile__email=email).exists():
            self.add_error(
                "email", "This email is already in registered. Please change email"
            )

        return cleaned_data

    def __init__(self, *args, **kwargs):

        super(StudentRegisterForm, self).__init__(*args, **kwargs)

        if not self.instance:

            self.fields.get("photo").widget.attrs["required"] = "required"
