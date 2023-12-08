from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from blog.models import Post, Comment
import random
from faker import Faker

fake = Faker()

class Command(BaseCommand):
    help = 'Populate the database with dummy data'

    def add_arguments(self, parser):
        parser.add_argument('posts', type=int, help='Number of blog posts to create')
        parser.add_argument('comments', type=int, help='Number of comments to create')

    def handle(self, *args, **options):
        num_posts = options['posts']
        num_comments = options['comments']

        # Create dummy users
        for _ in range(10):  # Adjust as needed
            User.objects.create(username=fake.user_name(), email=fake.email(), password=fake.password())

        # Create dummy posts
        for _ in range(num_posts):
            author = random.choice(User.objects.all())
            Post.objects.create(title=fake.sentence(), content=fake.paragraph(), author=author)

        # Create dummy comments
        for _ in range(num_comments):
            post = random.choice(Post.objects.all())
            author = random.choice(User.objects.all())
            Comment.objects.create(description=fake.paragraph(), post=post, created_by=author)

        self.stdout.write(self.style.SUCCESS(f'Successfully populated the database with {num_posts} posts and {num_comments} comments.'))
