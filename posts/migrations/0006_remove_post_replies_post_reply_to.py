# Generated by Django 4.2.6 on 2023-10-25 13:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0005_alter_post_embed'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='replies',
        ),
        migrations.AddField(
            model_name='post',
            name='reply_to',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='posts.post'),
        ),
    ]
