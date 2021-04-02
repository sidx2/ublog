from django.shortcuts import render,redirect
from django.http import HttpResponse
from blog.models import *
from django.contrib import messages
from .models import Users, Signup, BlogPost, BlogComment, Article, ArticleComment, Que, QueAns
from django.contrib.auth.models import User

import django.contrib.postgres

from django.contrib.auth  import authenticate, login, logout

from itertools import chain

# Create your views here.
def index(request):
	return render(request, 'blog/index.html')

def loginn(request):
	return render(request, 'blog/login.html')
	
def loggedin(request):
	
	if request.method == "POST":
		username = request.POST['username']
		password = request.POST['password']
		user=authenticate(username=username, password=password)
		if user is not None:
		        login(request, user)
		        messages.success(request, "Successfully Logged In")
		        return redirect("loginn")
		else:
		     messages.warning(request, "Invalid credentials! Please try again")
		     return redirect("loginn")	
				
				
	params = {
		'username':username
	}
	messages.success(request,'loggedin!')
	return render(request, 'blog/loggedin.html', params)
	
def signup(request):
	
	if request.method == "POST":
		fname = request.POST['fname']
		lname = request.POST['lname']
		email = request.POST['email']
		username = request.POST['username']
		pass1 = request.POST['pass1']
		pass2 = request.POST['pass2']
		
		if (" " in fname) or (" " in lname) or (" " in email) or (" " in username):
			messages.warning(request,'Fatal: Empty spaces are not allowed')
			return redirect("signup")
			
		if (not fname.isalnum()) or (not lname.isalnum()) or (not username.isalnum()):
			messages.warning(request,'Fatal: First Name, Last Name and username must be Alphanumeric!')
			return redirect("signup")
			
		if User.objects.filter(email=email).exists():
			messages.info(request,'Email is already in use!')
			return redirect("signup")
		
		if (not email.endswith('.com')):
			messages.info(request,'Email ID type is not accepted !')
			return redirect("signup")
		if(pass1!=pass2):
			messages.info(request,'Passwords do not match !')
			return redirect("signup")
			
		if User.objects.filter(username=username).exists():
			messages.info(request,'Username is already taken !')
			return redirect("signup")
		
		
		myuser = User.objects.create_user(username, email, pass1)
		myuser.first_name = fname
		myuser.last_name = lname
		myuser.save()
		messages.success(request, "Your UBlog account has been created successfully")
		return redirect('home')

		
		messages.success(request,'signup successful! ')
		
	return render(request, 'blog/signup.html')
	
def home(request):
	return render(request, 'blog/index.html')
	
def handleLogout(request):
	logout(request)
	messages.success(request,"You were Logged out !")
	return redirect("home")
	
def blog(request):
	blogs = BlogPost.objects.all().order_by('-id')[:10]
	
	params = {
		'blogs':blogs
	}
	return render(request, 'blog/blog.html',params)

def profile(request):
	if request.user != None:
		
		Bobj = BlogPost.objects.filter(author=request.user)
		articles = Article.objects.filter(author=request.user)
		
		Bobj.order_by('-id')
		articles.order_by('-id')
	
		params = {
			'posts':Bobj,
			'articles':articles
		}
		return render(request,'blog/profile.html',params)
	else:
		messages.warning(request,"You need to Login first")
		return redirect("loginn")
		
def startblog(request):
	
		
	return render(request, 'blog/startblog.html')

def handlestartblog(request):
	if request.method=="POST":
		bt = request.POST['blogtitle']
		bst = request.POST['blogsubtitle']
		bb = request.POST['blogbody']
		
		if (len(bt)<10) and (len(bst)<10) and (len(bb)<10):
			messages.warning(request,f'Failed to post your blog. Reason: spaming!')
			return redirect("startblog")
		
		obj = BlogPost(
			title=bt,
			subtitle=bst,
			body=bb,
			author=request.user
		)
		obj.save()
		red = obj.id
	messages.success(request,f'Your blog has been posted !')
	return redirect(f"blogpost/{red}")

	
def blogpost(request,slug):
	obj = BlogPost.objects.filter(id=slug).first()
	
	
	comments = BlogComment.objects.filter(asspost=obj,assparentcomment=None).order_by('-id')[:10]
	
	replies = BlogComment.objects.filter(asspost=obj).exclude(assparentcomment=None).order_by('-id')[:10]
	
	
	params = {
		'post':obj,
		'comments':comments,
		'replies':replies
	}
	return render(request,'blog/blogpost.html',params)	
#print(request.User)

def handlecomment(request):
	if request.method == "POST":
		postofcomment = request.POST['postofcomment']
		comment = request.POST['comment']
		
		commentor = request.user
		
		post = BlogPost.objects.filter(id=postofcomment).first()
		
		obj = BlogComment(
			comment=comment,
			commentor=commentor,
			asspost=post
		)
		obj.save()
		messages.success(request,'Your comment has been added successfully')
		return redirect(f"blogpost/{postofcomment}")
	
	
		
def handlereply(request):
	if request.method=="POST":
		postofcomment = request.POST['postofcomment']
		commentpr = request.POST['comment']
		parentofreply = request.POST['parentofreply']
		
		parentcomment = BlogComment.objects.filter(id=parentofreply).first()
		post = BlogPost.objects.filter(id=postofcomment).first()
		
		obj = BlogComment(
			comment=commentpr,
			commentor=request.user,
			asspost=post,
			assparentcomment=parentcomment
		)
		obj.save()
		messages.success(request,f'You replied to {parentcomment.commentor.first_name} {parentcomment.commentor.last_name}')
		return redirect(f"blogpost/{postofcomment}")
	
		

def publisharticle(request):
	return render(request,"blog/publisharticle.html")
	
def contactus(request):
	return render(request,"blog/postquestion.html")	
	
def handlepublisharticle(request):
	if request.method=="POST":
		heading = request.POST['heading']
		subheading = request.POST['subheading']
		content = request.POST['content']
		
		
		if (len(heading)<10) or (len(subheading)<10) or (len(content)<10):
			messages.warning(request,f'Failed to post your blog. Reason: spaming!')
			return redirect("publisharticle")
		obj = Article (
			heading=heading,
			subheading=subheading,
			content=content,
			author=request.user
		)
		
		obj.save()
		red = obj.id
		messages.success(request,'Your article has been published!')
		return redirect(f"article/{red}")
		
	return render(request,"blog/publisharticle.html")
	
def handlepostquestion(request):
	if request.method=="POST":
		question = request.POST['question']
		cat = request.POST['cat']
		
		obj = Que (
			category=cat,
			question=question,
			asker=request.user
		)
		obj.save()
		messages.success(request,'Your concern will be considered!')
		return redirect("home")
		
	return render(request,"blog/postquestion.html")
	
	
def article(request,slug):
	article = Article.objects.filter(id=slug).first()
	
	comments = ArticleComment.objects.filter(assarticle=article,assparentcomment=None).order_by('-id')[:10]
	
	replies = ArticleComment.objects.filter(assarticle=article).exclude(assparentcomment=None).order_by('-id')[:10]
	
	params = {
		'article':article,
		'comments':comments,
		'replies':replies
	}
	return render(request,"blog/article.html",params)

'''	
def question(request,slug):
	return HttpResponse(f"You r at question {slug}")
'''	
	
def handlearticlecomment(request):
	if request.method=="POST":
		comment = request.POST['comment']
		commentor = request.user
		articleofcomment = request.POST['articleofcomment']
		
		assarticle = Article.objects.filter(id=articleofcomment).first()
		
		obj = ArticleComment(
			comment=comment,
			commentor=commentor,
			assarticle=assarticle
		)
		
		obj.save()
		
		messages.success(request,'Comment added !')
		return redirect(f"article/{articleofcomment}")
		
		
def handlearticlereply(request):
	if request.method=="POST":
		articleofcomment = request.POST['articleofcomment']
		commentpr = request.POST['comment']
		parentofreply = request.POST['parentofreply']
		
		parentcomment = ArticleComment.objects.filter(id=parentofreply).first()
	
		article = Article.objects.filter(id=articleofcomment).first()
		
		obj = ArticleComment(
			comment=commentpr,
			commentor=request.user,
			assarticle=article,
			assparentcomment=parentcomment
		)
		obj.save()
		messages.success(request,f'You replied to {parentcomment.commentor.first_name} {parentcomment.commentor.last_name}')
		return redirect(f"article/{articleofcomment}")
		
		
def articles(request):
	articles = Article.objects.all().order_by('-id')[:10]
	
	params = {
		'articles':articles
	}
	
	return render(request,'blog/articles.html',params)

def bclogin(request):
	
	if request.method == "POST":
		username = request.POST['username']
		password = request.POST['password']
		postid = request.POST['postid']
		user=authenticate(username=username, password=password)
		if user is not None:
		        login(request, user)
		        messages.success(request, f"Logged in as {user.first_name} {user.last_name} \n Now you can comment !")
		        return redirect(f"blogpost/{postid}")
		else:
		     messages.warning(request, "Invalid credentials! Please try again")
		     return redirect(f"blogpost/{postid}")


def aclogin(request):
	
	if request.method == "POST":
		username = request.POST['username']
		password = request.POST['password']
		articleid = request.POST['articleid']
		user=authenticate(username=username, password=password)
		if user is not None:
		        login(request, user)
		        messages.success(request, f"Logged in as {user.first_name} {user.last_name} \n Now you can comment !")
		        return redirect(f"article/{articleid}")
		else:
		     messages.warning(request, "Invalid credentials! Please try again")
		     return redirect(f"article/{articleid}")

def about(request):
	return render(request,"blog/about.html")
	
def search(request):
	query = request.GET['query']
	
	bt = BlogPost.objects.filter(title__icontains=query).order_by('-id')[:10]
	bst = BlogPost.objects.filter(subtitle__icontains=query).order_by('-id')[:10]
	bufn = BlogPost.objects.filter(author__first_name__icontains=query).order_by('-id')[:10]
	buln = BlogPost.objects.filter(author__last_name__icontains=query).order_by('-id')[:10]
	
	blogss = (buln|bufn|bst|bt).distinct()
	blogs = blogss.order_by('-id')
	
	ah = Article.objects.filter(heading__icontains=query).order_by('-id')[:10]
	ash = Article.objects.filter(subheading__icontains=query).order_by('-id')[:10]
	aufn = Article.objects.filter(author__first_name__icontains=query).order_by('-id')[:10]
	auln = Article.objects.filter(author__last_name__icontains=query).order_by('-id')[:10]
	
	articles = (ah|ash |aufn|auln).distinct()

	params = {
		'query':query,
		'blogs':blogs,
		'articles':articles
	}
	return render(request,'blog/search.html',params)
	
		
def delblog(request):
	if request.method=="POST":
		blogid = request.POST['blogid']
		BlogPost.objects.filter(id=blogid).delete()
		messages.success(request,'Your Blog was deleted!')
		return redirect("home")

			
def delcom(request):
	if request.method=="POST":
		postid=request.POST['postid']
		comid=request.POST['comid']	
		
		BlogComment.objects.filter(id=comid).delete()
		
		messages.success(request,'Your comment was deleted!')
		return redirect(f"blogpost/{postid}")
		

def delart(request):
	if request.method=="POST":
		articleid = request.POST['articleid']
		Article.objects.filter(id=articleid).delete()
		messages.success(request,'Your Article was deleted!')
		return redirect("home")
		

def delcomart(request):
	if request.method=="POST":
		articleid=request.POST['articleid']
		comid=request.POST['comid']	
		
		ArticleComment.objects.filter(id=comid).delete()
		
		messages.success(request,'Your comment was deleted!')
		return redirect(f"article/{articleid}")
		
def delblogp(request):
	if request.method=="POST":
		blogid = request.POST['blogid']
		BlogPost.objects.filter(id=blogid).delete()
		messages.success(request,'Your Blog was deleted!')
		return redirect("profile")
		
		
def delartp(request):
	if request.method=="POST":
		articleid = request.POST['articleid']
		Article.objects.filter(id=articleid).delete()
		messages.success(request,'Your Article was deleted!')
		return redirect("profile")

	
def editarticle(request):
	if request.method=="POST":
		articleid=request.POST['articleid']
		obj = Article.objects.filter(id=articleid).first()
		params = {
			'article':obj
		}
	#	print(obj)
	#	print(obj.heading)
		return render(request,'blog/editarticle.html',params)
		

def updatearticle(request):
	if request.method=="POST":
		articleid=request.POST['articleid']
		heading=request.POST['heading']
		subheading=request.POST['subheading']
		content=request.POST['content']
		
		Article.objects.filter(id=articleid).update(heading=heading,subheading=subheading,content=content)
		
		messages.success(request,'Your Article has been updated!')	
		return redirect(f"article/{articleid}")

		
#edit blog		
def editblog(request):
	if request.method=="POST":
		blogid=request.POST['blogid']
		obj = BlogPost.objects.filter(id=blogid).first()
		params = {
			'blog':obj
		}
	#	print(obj)
	#	print(obj.heading)
		messages.warning(request,"The Glitch will be fixed ASAP, Don't interfare with HTML tags <>")
		return render(request,'blog/editblog.html',params)
		

def updateblog(request):
	if request.method=="POST":
		blogid=request.POST['blogid']
		title=request.POST['title']
		subtitle=request.POST['subtitle']
		body=request.POST['body']
		
		BlogPost.objects.filter(id=blogid).update(title=title,subtitle=subtitle,body=body)
		
		messages.success(request,'Your Blgo has been updated!')	
		return redirect(f"blogpost/{blogid}")