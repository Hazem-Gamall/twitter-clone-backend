# Generated by Django 4.2.6 on 2023-12-16 19:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("contenttypes", "0002_remove_content_type_name"),
        ("user_profile", "0018_notification"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="notification",
            name="issuer",
        ),
        migrations.AddField(
            model_name="notification",
            name="issuer_id",
            field=models.PositiveBigIntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="notification",
            name="issuer_type",
            field=models.ForeignKey(
                default=0,
                on_delete=django.db.models.deletion.CASCADE,
                to="contenttypes.contenttype",
            ),
            preserve_default=False,
        ),
    ]