from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.utils.timezone import now
# Create your models here.

class Users(models.Model):
	username = models.CharField(max_length=255)
	password=models.CharField(max_length=255)
	
	def __str__(self):
		return self.username

class Signup(models.Model):
	id = models.AutoField(primary_key=True)
	fname = models.CharField(max_length=48)
	lname = models.CharField(max_length=48)
	email = models.CharField(max_length=64)
	username = models.CharField(max_length=48)
	password = models.CharField(max_length=48)
	
	def __str__(self):
		return self.fname
		
class BlogPost(models.Model):
	id = models.AutoField(primary_key=True)
	title = models.CharField(max_length=512)
	subtitle = models.CharField(max_length=1024)
	body = models.TextField()
	author = models.ForeignKey(User, on_delete=models.CASCADE)
	timestamp = models.DateTimeField(default=now,blank=True)
	
class BlogComment(models.Model):
	id = models.AutoField(primary_key=True)
	comment = models.TextField()
	commentor = models.ForeignKey(User, on_delete=models.CASCADE)
	assparentcomment = models.ForeignKey('self',on_delete=models.CASCADE,null=True)
	asspost = models.ForeignKey(BlogPost,on_delete=models.CASCADE)
	timestamp = models.DateTimeField(default=now,blank=True)
	
class Article(models.Model):
	id = models.AutoField(primary_key=True)
	heading = models.TextField()
	subheading = models.TextField(null=True)
	content = models.TextField()
	author = models.ForeignKey(User, on_delete=models.CASCADE)
	
	timestamp = models.DateTimeField(default=now,blank=True)

class ArticleComment(models.Model):
	id = models.AutoField(primary_key=True)
	comment = models.TextField()
	commentor = models.ForeignKey(User, on_delete=models.CASCADE)
	assparentcomment = models.ForeignKey('self',on_delete=models.CASCADE,null=True)
	assarticle = models.ForeignKey(Article,on_delete=models.CASCADE)
	timestamp = models.DateTimeField(default=now,blank=True)
	
class Que(models.Model):
	id = models.AutoField(primary_key=True)
	category = models.CharField(max_length=64,null=True)
	question = models.TextField()
	asker = models.ForeignKey(User, on_delete=models.CASCADE)
	
	timestamp = models.DateTimeField(default=now,blank=True)
	
class QueAns(models.Model):
	id = models.AutoField(primary_key=True)
	comment = models.TextField()
	commentor = models.ForeignKey(User, on_delete=models.CASCADE)
	assparentcomment = models.ForeignKey('self',on_delete=models.CASCADE,null=True)
	assque = models.ForeignKey(BlogPost,on_delete=models.CASCADE)
	timestamp = models.DateTimeField(default=now,blank=True)
	

	