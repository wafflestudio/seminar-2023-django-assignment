# Generated by Django 4.2 on 2023-12-16 04:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chatbot', '0004_alter_character_first_message_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='character',
            name='image',
            field=models.FileField(blank=True, null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='chat',
            name='role',
            field=models.CharField(choices=[('A', 'assistant'), ('U', 'user')], max_length=10),
        ),
    ]
