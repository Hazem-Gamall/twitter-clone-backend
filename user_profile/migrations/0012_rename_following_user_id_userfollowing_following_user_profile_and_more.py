# Generated by Django 4.2.6 on 2023-10-28 12:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0011_alter_userfollowing_unique_together'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userfollowing',
            old_name='following_user_id',
            new_name='following_user_profile',
        ),
        migrations.RenameField(
            model_name='userfollowing',
            old_name='user_id',
            new_name='user_profile',
        ),
        migrations.AlterUniqueTogether(
            name='userfollowing',
            unique_together={('user_profile', 'following_user_profile')},
        ),
    ]
