# Generated by Django 4.1.3 on 2023-01-11 15:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0002_message'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='endtdatetime',
            field=models.DateTimeField(blank=True),
        ),
        migrations.AlterField(
            model_name='task',
            name='filter',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='task',
            name='message',
            field=models.CharField(blank=True, default='', max_length=500),
        ),
        migrations.AlterField(
            model_name='task',
            name='startdatetime',
            field=models.DateTimeField(blank=True),
        ),
    ]
