# Create your views here.
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer, UserSerializer, LoginSerializer

# default(NOT REST) 
from django.contrib.auth import authenticate, login, get_user_model

# Something is new for asgmt3
from rest_framework import status, permissions
from rest_framework.authtoken.models import Token
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.generics import get_object_or_404, ListCreateAPIView,RetrieveUpdateDestroyAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import CursorPagination

# get user models
User = get_user_model()

# 1. Login Logic
class LoginView(APIView):
   serializer_class = UserSerializer

   def post(self, request, format=None):
      serializer = LoginSerializer(data = request.data)
      username = request.data.get("username")
      password = request.data.get("password")

      # If username isn't given, then..
      if not username:
         return Response({"error": "이름, 곤란."}, status=status.HTTP_400_BAD_REQUEST)

      user = authenticate(request, username=username, password=password)

      # If user is vaild, then..
      if user is not None:
         login(request, user)
         token, created = Token.objects.get_or_create(user=user)
         return Response({"token": token.key}, status=status.HTTP_200_OK)

      return Response({"error": "그런 이상한 이름/PW를 가진 사람은 몰라."}, status=status.HTTP_400_BAD_REQUEST)

# 2. Sign Up Logic 
class SignUpView(CreateAPIView):
   serializer_class = UserSerializer

   def create(self, request, *args, **kwargs):
      serializer = self.get_serializer(data=request.data)
      serializer.is_valid(raise_exception=True)

      self.perform_create(serializer)
      user = serializer.instance
      token, created = Token.objects.get_or_create(user=user)

      return Response(
         {
         'user': UserSerializer(user, context=self.get_serializer_context()).data,
         'token': token.key
         }, 
      status=status.HTTP_201_CREATED)

# 3. Generic Pagination
class PostorCommentCursorPagination(CursorPagination):
   page_size = 10 
   ordering = '-dt_created'  # recently first

##### Post Implementations #####
# 4. Postlist (Just a list, Not detail)
class PostList(ListCreateAPIView):
   queryset = Post.objects.all()
   serializer_class = PostSerializer
   permission_classes = [IsAuthenticated]
   pagination_class = PostorCommentCursorPagination
   authentication_classes = [SessionAuthentication, TokenAuthentication]

   def get_permissions(self):
      if self.request.method == "POST":
         return [IsAuthenticated()]
      return []

   def perform_create(self, serializer):
      serializer.save(author=self.request.user)

# 5. Postlist <- Tag
class PostListByTag(ListAPIView):
   serializer_class = PostSerializer
   pagination_class = PostorCommentCursorPagination
   authentication_classes = [SessionAuthentication, TokenAuthentication]

   def get_queryset(self):
      tag_name = self.kwargs.get('tag_name')
      return Post.objects.filter(tag__name=tag_name)

# 6. Authentication for Write Permissions
class IsAuthorOrReadOnly(permissions.BasePermission):
   def has_object_permission(self, request, view, obj):
      # this case means "read"
      if request.method in permissions.SAFE_METHODS:
         return True
      
      # this case means "write"
      # We have to check if writor or not
      return obj.author == request.user
   
# 7. Post Detail (Update and Delete)
class PostDetail(RetrieveUpdateDestroyAPIView):
   queryset = Post.objects.all()
   serializer_class = PostSerializer
   permission_classes = [IsAuthorOrReadOnly]
   authentication_classes = [SessionAuthentication, TokenAuthentication]

##### Comment Implementations #####
# 8. Commentlist (Just a list, Not detail)
class CommentList(ListCreateAPIView):
   queryset = Comment.objects.all()
   serializer_class = CommentSerializer
   permission_classes = [IsAuthenticated]
   pagination_class = PostorCommentCursorPagination
   authentication_classes = [SessionAuthentication, TokenAuthentication]
    
   def get_permissions(self):
      if self.request.method == "POST":
         return [IsAuthenticated()]
      return []
    
   def perform_create(self, serializer):
      serializer.save(author=self.request.user)

# 9. CommentList <- Tag 
class CommentListByPost(ListAPIView):
   serializer_class =  CommentSerializer
   pagination_class = PostorCommentCursorPagination
   authentication_classes = [SessionAuthentication, TokenAuthentication]

   def get_queryset(self):
      post_id = self.kwargs.get('post_id')
      if post_id is not None:
         return Comment.objects.filter(post__id=post_id)
      return Comment.objects.all()

# 10. CommentList <- Tag 
class CommentListByTag(ListAPIView):
   serializer_class = CommentSerializer
   pagination_class = PostorCommentCursorPagination
   authentication_classes = [SessionAuthentication, TokenAuthentication]

   def get_queryset(self):
      tag_name = self.kwargs.get('tag_name')
      return Comment.objects.filter(tag__name=tag_name)

# 11. Comment Detail (Update and Delete)
class CommentDetail(RetrieveUpdateDestroyAPIView):
   queryset = Comment.objects.all()
   serializer_class = CommentSerializer
   permission_classes = [IsAuthorOrReadOnly]
   authentication_classes = [SessionAuthentication, TokenAuthentication]