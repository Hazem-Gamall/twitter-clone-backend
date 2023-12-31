# Generated by Django 4.2.6 on 2023-12-25 18:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0007_alter_message_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='chat',
            options={'ordering': ['messages']},
        ),
        migrations.AddField(
            model_name='message',
            name='seen',
            field=models.BooleanField(default=True),
            preserve_default=False,
        ),
    ]
