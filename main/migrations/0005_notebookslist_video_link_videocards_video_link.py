# Generated by Django 4.0.4 on 2022-05-17 07:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_videocards'),
    ]

    operations = [
        migrations.AddField(
            model_name='notebookslist',
            name='video_link',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='videocards',
            name='video_link',
            field=models.TextField(blank=True, null=True),
        ),
    ]
