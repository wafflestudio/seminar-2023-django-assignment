# Generated by Django 4.2.5 on 2023-11-06 12:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_alter_post_dt_created_alter_post_dt_updated_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='author',
            field=models.CharField(max_length=40),
        ),
        migrations.AlterField(
            model_name='comment',
            name='created_at',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='comment',
            name='updated_at',
            field=models.DateField(),
        ),
    ]