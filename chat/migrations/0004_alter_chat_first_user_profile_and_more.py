# Generated by Django 4.2.6 on 2023-11-15 14:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0017_alter_mention_post'),
        ('chat', '0003_chat_first_user_profile_chat_second_user_profile_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chat',
            name='first_user_profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='chat_set1', to='user_profile.userprofile'),
        ),
        migrations.AlterField(
            model_name='chat',
            name='second_user_profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='chat_set2', to='user_profile.userprofile'),
        ),
    ]