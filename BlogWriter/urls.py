from django.urls import path
from . views import *
urlpatterns=[
    path("",HomePage,name="HomePage"),
    path("blog/<int:blog_id>/",BlogDetail,name="BlogDetail"),
    path('create-edit-blog/', CreateEditBlog, name='CreateEditBlog'),
    path('blog-tldr/<int:blog_id>/', blog_tldr, name='blog_tldr'), 
    path("accounts/login/", login_view, name="login"),
    path("accounts/register/", register_view, name="register"),
    path('accounts/logout/', logout_view, name='logout'),
    path('edit-blog/<int:blog_id>/', CreateEditBlog, name='EditBlog'),
    path('delete-blog/<int:blog_id>/', DeleteBlog, name='DeleteBlog'),

]