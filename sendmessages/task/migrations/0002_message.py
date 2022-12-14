# Generated by Django 4.1.3 on 2022-12-25 11:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0001_initial'),
        ('task', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sentdatetime', models.DateTimeField()),
                ('status', models.BooleanField(default=False, max_length=20)),
                ('client', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='clients', to='client.client')),
                ('task', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='tasks', to='task.task')),
            ],
        ),
    ]
