from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="index"),
    path('loginn',views.loginn, name='loginn'),
    path('loggedin',views.loggedin,name='loggedin'),
    path('signup', views.signup,name="signup"),
    path('home',views.home,name="home"),
    path('handleLogout',views.handleLogout,name="handleLogout"),
    path('blog',views.blog,name="blog"),
    path('profile',views.profile,name="profile"),
    path('startblog',views.startblog,name="startblog"),
    path('handlestartblog',views.handlestartblog,name="handlestartblog"),
    
    # slugs
    path('blogpost/<slug:slug>',views.blogpost,name="blogpost"),
    path('article/<slug:slug>',views.article,name="article"),
    path('',views.home,name="home"),
    path('handlecomment',views.handlecomment,name="handlecomment"),
    path('handlereply',views.handlereply,name="handlereply"),
    
    path('publisharticle',views.publisharticle,name="publisharticle"),
    path('contactus',views.contactus,name="contactus"),
    
    path('handlepublisharticle',views.handlepublisharticle,name="handlepublisharticle"),
    path('handlepostquestion',views.handlepostquestion,name="handlepostquestion"),
    
    path('handlearticlecomment',views.handlearticlecomment,name="handlearticlecomment"),
    
    path('handlearticlereply',views.handlearticlereply,name="handlearticlereply"),
    path('articles',views.articles,name="articles"),
    path('bclogin',views.bclogin,name="bclogin"),
    path('aclogin',views.aclogin,name="aclogin"),
    path('about',views.about,name="about"),
    path('search',views.search,name="search"),
    path('delblog',views.delblog,name="delblog"),
    path('delcom',views.delcom,name="delcom"),
    path('delart',views.delart,name="delart"),
    path('delcomart',views.delcomart,name="delcomart"),
    path('delblogp',views.delblogp),
    path('delartp',views.delartp,name="delartp"),
    path('editarticle',views.editarticle,name="editarticle"),
    path('updatearticle',views.updatearticle,name="updatearticle"),
    path('editblog',views.editblog,name="editblog"),
    path('updateblog',views.updateblog,name="updateblog")
    
    
  
]