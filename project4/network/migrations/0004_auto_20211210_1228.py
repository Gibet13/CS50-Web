# Generated by Django 3.2.9 on 2021-12-10 11:28

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0003_follower'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='follower',
            name='following',
        ),
        migrations.AddField(
            model_name='follower',
            name='following',
            field=models.ManyToManyField(blank=True, related_name='followers', to=settings.AUTH_USER_MODEL),
        ),
    ]