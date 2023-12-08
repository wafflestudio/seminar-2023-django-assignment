# populate_data.py

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from blog.models import Post, Comment, Tag
from faker import Faker
import random

fake = Faker()


class Command(BaseCommand):
    help = 'Populate the database with dummy data'

    def add_arguments(self, parser):
        parser.add_argument('posts', type=int, help='Number of posts to create')
        parser.add_argument('comments', type=int, help='Number of comments to create')

    def handle(self, *args, **options):
        num_posts = options['posts']
        num_comments = options['comments']

        # Create tags
        tags = [Tag.objects.create(content=fake.word()) for _ in range(5)]  # Create 5 tags

        # Create users
        password = 'test'  # Set a single password for all users
        users = [User.objects.create(username=fake.user_name(), password=password) for _ in range(5)]  # Create 5 users

        # Create posts
        for _ in range(num_posts):
            post = Post.objects.create(
                title=fake.sentence(),
                description=fake.paragraph(),
                created_by=random.choice(users)
            )
            post.tags.set(random.sample(tags, random.randint(1, len(tags))))

            # Create comments for each post
            for _ in range(num_comments):
                comment = Comment.objects.create(
                    description=fake.text(),
                    post=post,
                    created_by=random.choice(users)
                )
                comment.tags.set(random.sample(tags, random.randint(1, len(tags))))

        self.stdout.write(self.style.SUCCESS(f'Successfully populated the database with {num_posts} posts and {num_comments} comments.'))
