# Generated by Django 4.1.3 on 2022-12-08 16:10

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('startdatetime', models.DateTimeField()),
                ('endtdatetime', models.DateTimeField()),
                ('message', models.CharField(default='', max_length=500)),
                ('filter', models.CharField(default='', max_length=100)),
                ('status', models.CharField(default='', max_length=20)),
                ('status_text', models.CharField(default='', max_length=500)),
            ],
        ),
    ]
