# Generated by Django 4.0.4 on 2022-10-26 17:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0044_alter_documentofsold_username'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderlist',
            name='data',
            field=models.DateField(auto_now=True),
        ),
    ]
