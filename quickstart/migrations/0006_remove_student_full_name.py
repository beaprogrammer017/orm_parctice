# Generated by Django 3.2.10 on 2024-05-13 16:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quickstart', '0005_student_full_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='full_name',
        ),
    ]