# Generated by Django 4.2.7 on 2023-11-20 20:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_remove_tag_comments_remove_tag_posts_comment_tags_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='tags',
            field=models.ManyToManyField(related_name='comments', to='blog.tag'),
        ),
    ]