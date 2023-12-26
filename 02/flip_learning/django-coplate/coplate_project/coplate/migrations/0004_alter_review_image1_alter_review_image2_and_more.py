# Generated by Django 4.2 on 2023-11-18 05:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coplate', '0003_review_alter_user_nickname'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='image1',
            field=models.ImageField(upload_to='review_pics'),
        ),
        migrations.AlterField(
            model_name='review',
            name='image2',
            field=models.ImageField(blank=True, upload_to='review_pics'),
        ),
        migrations.AlterField(
            model_name='review',
            name='image3',
            field=models.ImageField(blank=True, upload_to='review_pics'),
        ),
    ]
