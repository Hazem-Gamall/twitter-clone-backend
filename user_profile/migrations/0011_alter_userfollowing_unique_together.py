# Generated by Django 4.2.6 on 2023-10-28 11:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0010_userprofile_liked_posts'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='userfollowing',
            unique_together={('user_id', 'following_user_id')},
        ),
    ]
