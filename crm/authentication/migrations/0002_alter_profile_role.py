# Generated by Django 5.1.6 on 2025-06-01 05:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='role',
            field=models.CharField(choices=[('admin', 'Admin'), ('student', 'Student'), ('academic_counselor', 'Academic Counselor'), ('trainer', 'Trainer'), ('sales', 'Sales')], default='student', max_length=30),
        ),
    ]
