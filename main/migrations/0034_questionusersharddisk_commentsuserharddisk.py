# Generated by Django 4.0.4 on 2022-10-02 16:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0033_harddisklists'),
    ]

    operations = [
        migrations.CreateModel(
            name='QuestionUsersHardDisk',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_of_user', models.CharField(max_length=50)),
                ('comment', models.TextField()),
                ('date', models.DateField(auto_now=True)),
                ('name_of_stuff', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.harddisklists')),
            ],
            options={
                'verbose_name': 'QuestionUsersHardDisk',
                'verbose_name_plural': 'QuestionUsersHardDisk',
            },
        ),
        migrations.CreateModel(
            name='CommentsUserHardDisk',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.IntegerField(blank=True, choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)], null=True)),
                ('name_of_user', models.CharField(max_length=50)),
                ('comment', models.TextField()),
                ('link_video', models.TextField(blank=True, null=True)),
                ('date', models.DateField(auto_now=True)),
                ('name_of_stuff', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.harddisklists')),
            ],
            options={
                'verbose_name': 'CommentsUserHardDisk',
                'verbose_name_plural': 'CommentsUserHardDisk',
            },
        ),
    ]
