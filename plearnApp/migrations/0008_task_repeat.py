# Generated by Django 5.1.6 on 2025-04-15 07:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plearnApp', '0007_task_notified'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='repeat',
            field=models.CharField(choices=[('Once', 'Once'), ('Daily', 'Daily'), ('Weekly', 'Weekly'), ('Monthly', 'Monthly')], default='Once', max_length=10),
        ),
    ]
