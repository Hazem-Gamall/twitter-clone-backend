# Generated by Django 4.2.6 on 2023-10-23 11:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0007_userprofile_bio'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='bio',
            field=models.CharField(blank=True, default='', max_length=160),
        ),
    ]
