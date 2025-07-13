from django.db import models

# Create your models here.

from django.contrib.auth.models import AbstractUser


class RoleChoices(models.TextChoices):

    ADMIN = "admin", "Admin"

    STUDENT = "student", "Student"

    ACADEMIC_COUNSELLOR = "academic_counselor", "Academic Counselor"

    TRAINER = "trainer", "Trainer"

    SALES = "sales", "Sales"

class Profile(AbstractUser):
    """
    Custom user model that extends the default Django user model.
    """

    # Add any additional fields you want to include in your custom user model
    role = models.CharField(
        max_length=30,
        choices=RoleChoices.choices,
        default=RoleChoices.STUDENT,
    )

    def __str__(self):

        return f"{self.username} - {self.role}"

    class Meta:
        verbose_name = "Profile"
        verbose_name_plural = "Profile"
