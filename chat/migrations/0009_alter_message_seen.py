# Generated by Django 4.2.6 on 2023-12-25 18:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0008_alter_chat_options_message_seen'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='seen',
            field=models.BooleanField(default=False),
        ),
    ]
