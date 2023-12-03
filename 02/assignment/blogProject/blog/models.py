from django.db import models

# Create your models here.
class Post(models.Model):
   id = models.AutoField(),
   title = models.CharField(max_length=100)
   description = models.TextField()
   updated_at = models.DateTimeField(auto_now=True)
   created_at = models.DateTimeField(auto_now_add=True)
   created_by = models.ForeignKey("blogauth.User", on_delete = models.CASCADE)

   class Meta:
      verbose_name = "글"
      verbose_name_plural = "글 목록"

class Comment(models.Model):
   #related name으로 foreignkey를 사용해 가져올 때의 이름을 설정
   post = models.ForeignKey(Post, on_delete = models.CASCADE, related_name='comments')
   description = models.TextField()
   updated_at = models.DateTimeField(auto_now=True)
   created_at = models.DateTimeField(auto_now_add=True)
   created_by = models.ForeignKey("blogauth.User", on_delete = models.CASCADE)

   class Meta:
      verbose_name = "댓글"
      verbose_name_plural = "댓글 목록" 
