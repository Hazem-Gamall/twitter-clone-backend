# Generated by Django 4.2.6 on 2023-12-16 18:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0017_alter_mention_post'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notification_type', models.CharField(choices=[('R', 'Reply'), ('T', 'Repost'), ('L', 'Like'), ('M', 'Mention')], max_length=1)),
                ('creation', models.DateTimeField(auto_now_add=True)),
                ('viewed', models.BooleanField(default=False)),
                ('issuer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user_profile.userprofile')),
                ('reciever', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notifications', to='user_profile.userprofile')),
            ],
        ),
    ]
