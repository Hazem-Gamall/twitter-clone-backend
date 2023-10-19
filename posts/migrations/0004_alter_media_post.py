# Generated by Django 4.2.6 on 2023-10-18 19:27

from django.db import migrations, models
import django.db.models.deletion
import posts.models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0003_alter_post_embed_alter_post_replies'),
    ]

    operations = [
        migrations.AlterField(
            model_name='media',
            name='post',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='media', to='posts.post', validators=[posts.models.restrict_media]),
        ),
    ]
