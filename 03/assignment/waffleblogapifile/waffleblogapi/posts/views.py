from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from rest_framework.authtoken.models import Token
from rest_framework import status

from .models import User, Post, Comment
from .serializers import UserSerializer, PostSerializer, CommentSerializer

@api_view(['GET', 'POST'])
def user_list(request):
  if request.method == 'GET':
    return get_users(request)
  elif request.method == 'POST':
    return create_user(request)
  else:
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
  
@api_view(['POST'])
def register(request):
  return create_user(request)
  

def get_users(request):
  users = User.objects.all()
  serializer = UserSerializer(users, many=True)
  return Response(serializer.data)

def create_user(request):
  serializer = UserSerializer(data=request.data)
  if serializer.is_valid():
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)
  else:
    return Response(status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['POST'])
def login(request):
  serializer = UserSerializer(data=request.data)
  if not serializer.is_valid():
    return Response(status=status.HTTP_400_BAD_REQUEST)
  if not User.objects.filter(username=serializer.data['username']).exists():
    return Response(status=status.HTTP_400_BAD_REQUEST)
  user = User.objects.get(username=serializer.data['username'])
  if not user.check_password(serializer.data['password']):
    return Response(status=status.HTTP_400_BAD_REQUEST)
  token, created = Token.objects.get_or_create(user=user)
  return Response({'token': token.key})



@api_view(['GET', 'POST'])
def post_list(request):
  if request.method == 'GET':
    return get_posts(request)
  elif request.method == 'POST':
    return create_post(request)
  else:
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
  

@api_view(['GET'])
def post_list_by_tag(request, tag):
  posts = Post.objects.filter(tags__content=tag)
  serializer = PostSerializer(posts, many=True)
  return Response(serializer.data)


def get_posts(request):
  posts = Post.objects.all()
  for post in posts:
    post.content = post.content.slice([0, 300])
  serializer = PostSerializer(posts, many=True)
  return Response(serializer.data)

def create_post(request):
  serializer = PostSerializer(data=request.data)
  if serializer.is_valid():
    serializer.author = request.user
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)
  else:
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  


@api_view(['GET', 'PATCH', 'DELETE'])
def post_detail(request, post_id):
  post = get_object_or_404(Post, pk=post_id)

  if request.method == 'GET':
    return get_post(request, post)
  elif request.method == 'PATCH':
    return update_post(request, post)
  elif request.method == 'DELETE':
    return delete_post(request, post)
  else:
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


def get_post(request, post):
  serializer = PostSerializer(post)
  serializer.data['content'] = serializer.data['content'].split('\n')
  return Response(serializer.data)

def update_post(request, post):
  serializer = PostSerializer(post, data=request.data, partial=True)
  if post.author != request.user:
    return Response(status=status.HTTP_403_FORBIDDEN)
  if serializer.is_valid():
    serializer.save()
    return Response(serializer.data)
  else:
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def delete_post(request, post):
  if post.author != request.user:
    return Response(status=status.HTTP_403_FORBIDDEN)
  for tag in post.tags.all():
    if tag.posts.count() == 1:
      tag.delete()
  post.delete()
  return Response(status=status.HTTP_204_NO_CONTENT)



@api_view(['GET'])
def all_comment_list(request):
  comments = Comment.objects.all()
  serializer = CommentSerializer(comments, many=True)
  return Response(serializer.data)

@api_view(['GET'])
def comment_list_by_tag(request, tag):
  comments = Comment.objects.filter(tags__content=tag)
  serializer = CommentSerializer(comments, many=True)
  return Response(serializer.data)


@api_view(['GET', 'POST'])
def comment_list(request, post_id):
  if request.method == 'GET':
    return get_comments(request, post_id)
  elif request.method == 'POST':
    return create_comment(request, post_id)
  else:
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


def get_comments(request, post_id):
  post = get_object_or_404(Post, pk=post_id)
  comments = post.comment_set.all()
  serializer = CommentSerializer(comments, many=True)
  return Response(serializer.data)

def create_comment(request, post_id):
  post = get_object_or_404(Post, pk=post_id)
  serializer = CommentSerializer(data=request.data)
  if serializer.is_valid():
    serializer.author = request.user
    serializer.post = post
    return Response(serializer.data, status=status.HTTP_201_CREATED)
  else:
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  

@api_view(['GET', 'PATCH', 'DELETE'])
def comment_detail(request, comment_id):
  comment = get_object_or_404(Comment, pk=comment_id)

  if request.method == 'GET':
    return get_comment(request, comment)
  elif request.method == 'PATCH':
    return update_comment(request, comment)
  elif request.method == 'DELETE':
    return delete_comment(request, comment)
  else:
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

def get_comment(request, comment):
  serializer = CommentSerializer(comment)
  return Response(serializer.data)

def update_comment(request, comment):
  serializer = CommentSerializer(comment, data=request.data, partial=True)
  if comment.author != request.user:
    return Response(status=status.HTTP_403_FORBIDDEN)
  if serializer.is_valid():
    serializer.save()
    return Response(serializer.data)
  else:
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  

def delete_comment(request, comment):
  if comment.author != request.user:
    return Response(status=status.HTTP_403_FORBIDDEN)
  for tag in comment.tags.all():
    if tag.comments.count() == 1:
      tag.delete()
  comment.delete()
  return Response(status=status.HTTP_204_NO_CONTENT)
