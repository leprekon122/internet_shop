# Generated by Django 4.0.4 on 2022-10-26 10:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0042_orderlist_order_num'),
    ]

    operations = [
        migrations.CreateModel(
            name='DocumentOfSold',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=60)),
                ('sur_name', models.CharField(max_length=60)),
                ('mobile_number', models.CharField(max_length=60)),
                ('email', models.EmailField(max_length=60)),
                ('product_title', models.CharField(max_length=255)),
                ('product_pic', models.TextField()),
                ('product_price', models.IntegerField()),
                ('order_num', models.CharField(blank=True, max_length=255, null=True)),
                ('username', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'DocumentOfSold',
                'verbose_name_plural': 'DocumentOfSold',
            },
        ),
    ]