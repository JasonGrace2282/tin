# Generated by Django 2.2.3 on 2019-07-30 19:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('submissions', '0010_auto_20190730_1546'),
    ]

    operations = [
        migrations.AlterField(
            model_name='submission',
            name='points_received',
            field=models.DecimalField(blank=True, decimal_places=3, max_digits=6, null=True),
        ),
    ]
