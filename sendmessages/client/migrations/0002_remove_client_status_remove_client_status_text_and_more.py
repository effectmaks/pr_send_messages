# Generated by Django 4.1.3 on 2022-12-25 12:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='client',
            name='status',
        ),
        migrations.RemoveField(
            model_name='client',
            name='status_text',
        ),
        migrations.AddField(
            model_name='client',
            name='utc',
            field=models.IntegerField(default=0),
        ),
    ]