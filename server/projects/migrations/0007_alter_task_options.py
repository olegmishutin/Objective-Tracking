# Generated by Django 5.0.6 on 2024-05-30 13:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0006_alter_task_executor'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='task',
            options={'ordering': ['-created_at'], 'verbose_name': 'Задача', 'verbose_name_plural': 'Задачи'},
        ),
    ]