from django.urls import path
from . views import *
urlpatterns = [
    path("", HomePage, name="HomePage"),
    path("blog/<int:blog_id>/", BlogDetail, name="BlogDetail"),
    path("blog/create/", CreateEditBlog, name="CreateEditBlog"),
    path("blog/edit/<int:blog_id>/", CreateEditBlog, name="EditBlog"),
    path("blog/delete/<int:blog_id>/", DeleteBlog, name="DeleteBlog"),
    path("blog/tldr/<int:blog_id>/", blog_tldr, name="blog_tldr"),
    path('blog/<int:blog_id>/comment/', add_comment, name='add_comment'),
    path('blog/<int:blog_id>/like/', toggle_like, name='toggle_like'),
    path("my-blogs/", my_blogs, name="MyBlogs"),
    path("accounts/login/", login_view, name="login"),
    path("accounts/register/", register_view, name="register"),
    path("accounts/logout/", logout_view, name="logout"),
    
]
