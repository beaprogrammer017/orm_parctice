# Generated by Django 3.2.10 on 2024-05-13 16:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quickstart', '0002_student'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='full_name',
            field=models.CharField(default=0, max_length=200),
            preserve_default=False,
        ),
    ]