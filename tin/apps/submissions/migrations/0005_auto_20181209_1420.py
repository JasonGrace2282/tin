# Generated by Django 2.1.4 on 2018-12-09 19:20

from django.db import migrations, models
import tin.apps.submissions.models


class Migration(migrations.Migration):

    dependencies = [
        ('submissions', '0004_auto_20181208_1123'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='submission',
            name='filename',
        ),
        migrations.AddField(
            model_name='submission',
            name='file',
            field=models.FileField(null=True, upload_to=tin.apps.submissions.models.upload_submission_file_path),
        ),
    ]