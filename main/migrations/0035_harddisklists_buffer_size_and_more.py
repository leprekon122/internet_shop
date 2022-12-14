# Generated by Django 4.0.4 on 2022-10-04 08:56

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0034_questionusersharddisk_commentsuserharddisk'),
    ]

    operations = [
        migrations.AddField(
            model_name='harddisklists',
            name='buffer_size',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='harddisklists',
            name='count_of_twist',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name='harddisklists',
            name='size',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='harddisklists',
            name='socket',
            field=models.CharField(default=django.utils.timezone.now, max_length=50),
            preserve_default=False,
        ),
    ]
