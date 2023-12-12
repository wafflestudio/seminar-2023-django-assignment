from django.test import TestCase

# Create your tests here

#Import model first
from .models import Post, Comment, Tag

#Third-party app imports
from model_mommy import mommy

#Generates Test cases
post = mommy.make('blog.Post', _quantity = 100)
comment = mommy.make('blog.Comment', _quantity = 100)
tag = mommy.make('blog.Tag', _quantity = 100)