# Generated by Django 2.2 on 2019-04-19 04:45

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TodoItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=280, null=True)),
                ('date_created', models.DateTimeField(verbose_name='date created')),
                ('date_due', models.DateTimeField(verbose_name='date due')),
                ('date_doing', models.DateTimeField(null=True, verbose_name='date doing')),
                ('priority_level', models.IntegerField(default=0)),
                ('catagory', models.IntegerField(default=0)),
                ('is_done', models.BooleanField(default=False)),
                ('showAlways', models.BooleanField(default=False)),
            ],
        ),
    ]