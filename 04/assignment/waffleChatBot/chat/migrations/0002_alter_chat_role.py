# Generated by Django 4.1 on 2023-12-14 11:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chat',
            name='role',
            field=models.CharField(choices=[('assistant', 'assistant'), ('user', 'user')], max_length=10),
        ),
    ]
