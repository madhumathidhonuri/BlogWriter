from django.db import models
from django.contrib.auth.models import User

class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    summary = models.TextField(blank=True,null=True) 
    tags = models.ManyToManyField('Tag',related_name="posts")
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def word_count(self):
        return len(self.content.split())
    def reading_time(self):
        return round(self.word_count()/200)
    
class Tag(models.Model):
    name = models.CharField(max_length=50,unique=True)
    def __str__(self):
        return self.name
    
class UserProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    favorite_tags = models.ManyToManyField('Tag',blank=True,related_name="interested_users")
    def __str__(self):
        return self.user.username