# Generated by Django 3.0.2 on 2020-04-10 02:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meeting', '0015_meeting_final_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='meeting',
            name='final_date',
            field=models.DateTimeField(),
        ),
    ]
