from django.db import models

import uuid

# Create your models here.


class BaseClass(models.Model):

    uuid = models.SlugField(unique=True, default=uuid.uuid4)

    active_status = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:

        abstract = True


class CourseChoices(models.TextChoices):

    PY_DJANGO = "PY-DJANGO", "PY-DJANGO"

    MEARN = "MEARN", "MEARN"

    DATA_SCIENCE = "DATA SCIENCE", "DATA SCIENCE"

    SOFTWARE_TESTING = "SOFTWARE TESTING", "SOFTWARE TESTING"


class DistrictChoices(models.TextChoices):

    THIRUVANANTHAPURAM = "Thiruvananthapuram", "Thiruvananthapuram"

    KOLLAM = "Kollam", "Kollam"

    PATHANAMTHITTA = "Pathanamthitta", "Pathanamthitta"

    ALAPPUZHA = "Alappuzha", "Alappuzha"

    KOTTAYAM = "Kottayam", "Kottayam"

    IDUKKI = "Idukki", "Idukki"

    ERNAKULAM = "Ernakulam", "Ernakulam"

    THRISSUR = "Thrissur", "Thrissur"

    PALAKKAD = "Palakkad", "Palakkad"

    MALAPPURAM = "Malappuram", "Malappuram"

    KOZHIKKOD = "Kozhikkod", "Kozhikkod"

    VAYANADU = "Vayanadu", "Vayanadu"

    KANNUR = "Kannur", "Kannur"

    KAZARGOD = "Kazargod", "Kazargod"


class BatchChoices(models.TextChoices):

    PY_NOV_2024 = "PY-NOV-2024", "PY-NOV-2024"

    PY_JAN_2025 = "PY-JAN-2025", "PY-JAN-2025"

    DS_JAN_2025 = "DS-JAN-2025", "DS-JAN-2025"

    ST_JAN_2025 = "ST-JAN-2025", "ST-JAN-2025"

    MEARN_NOV_2024 = "MEARN-NOV-2024", "MEARN-NOV-2024"

    MEARN_JAN_2025 = "MEARN-JAN-2025", "MEARN-JAN-2025"


class TrainerChoices(models.TextChoices):

    JOHN_DOE = "John Doe", "John Doe"

    JAMES = "James", "James"

    JANE = "Jane", "Jane"

    ALEX = "Alex", "Alex"


class Students(BaseClass):
    profile = models.OneToOneField('authentication.Profile', on_delete=models.CASCADE)

    first_name = models.CharField(max_length=50)

    second_name = models.CharField(max_length=50)

    photo = models.ImageField(upload_to="students")

    email = models.EmailField(unique=True, null=True, blank=True)

    contact = models.CharField(max_length=15)

    house_name = models.CharField(max_length=25)

    post_office = models.CharField(max_length=25)

    district = models.CharField(max_length=25, choices=DistrictChoices.choices)

    pincode = models.CharField(max_length=6)

    adm_number = models.CharField(max_length=50)

    # course = models.CharField(max_length=25, choices=CourseChoices.choices)

    course = models.ForeignKey(
        "courses.Courses", on_delete=models.SET_NULL, null=True, blank=True
    )

    # batch = models.CharField(max_length=25, choices=BatchChoices.choices)

    batch = models.ForeignKey(
        "batches.Batches", on_delete=models.SET_NULL, null=True, blank=True
    )

    # batch_date = models.DateField()

    join_date = models.DateField(auto_now_add=True)

    # trainer_name = models.CharField(
    # max_length=25,
    # choices=TrainerChoices.choices
    # )

    trainer = models.ForeignKey(
        "trainers.Trainers", on_delete=models.SET_NULL, null=True, blank=True
    )

    def __str__(self):

        return f"{self.first_name} {self.second_name} {self.batch}"

    class Meta:

        verbose_name = "Students"

        verbose_name_plural = "Students"

        ordering = ["id"]
