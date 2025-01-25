from django.urls import path
from . import views
urlpatterns=[
    path('',views.home,name="home"),
    path('signup/',views.signup,name="signup"),
    path('signin/',views.signin,name="signin"),
    path('blog/',views.blog,name="blog"),
    path('write/', views.write_blog, name='write_blog'), 
    path('logout/',views.logout,name="logout"),
    path('profile/',views.profile,name='profile'),
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),
    path('post/delete/<int:post_id>/', views.delete_blog, name='delete_blog'),
]