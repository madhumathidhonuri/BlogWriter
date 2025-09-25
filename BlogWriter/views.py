from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import BlogPost, Tag, Comment, Like
from .forms import CustomUserCreationForm, BlogPostForm
from transformers import pipeline
import json

summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")

def HomePage(request):
    blogs = BlogPost.objects.all().order_by('-created_at')
    return render(request, "HomePage.html", {"blogs": blogs})


def BlogDetail(request, blog_id):
    blog = get_object_or_404(BlogPost, id=blog_id)
    related_blogs = []
    first_tag = blog.tags.first()
    if first_tag:
        related_blogs = first_tag.posts.exclude(id=blog.id)[:3]
    comments = Comment.objects.filter(post=blog).order_by('-created_at')
    user_liked = False
    if request.user.is_authenticated:
        user_liked = Like.objects.filter(post=blog, user=request.user).exists()
    return render(request, "BlogDetail.html", {
        "blog": blog,
        "related_blogs": related_blogs,
        "comments": comments,
        "user_liked": user_liked
    })


def CreateEditBlog(request, blog_id=None):
    if blog_id:
        blog = get_object_or_404(BlogPost, id=blog_id)
        if blog.author != request.user:
            messages.error(request, "You cannot edit this blog.")
            return redirect('HomePage')
    else:
        blog = None

    if request.method == 'POST':
        form = BlogPostForm(request.POST, instance=blog)
        if form.is_valid():
            new_blog = form.save(commit=False)
            if not blog:
                new_blog.author = request.user
            new_blog.save()
            tags_str = form.cleaned_data.get('tags_input', '')
            tags_list = [t.strip() for t in tags_str.split(',') if t.strip()]
            tag_objs = []
            for tag_name in tags_list:
                tag_obj, created = Tag.objects.get_or_create(name=tag_name)
                tag_objs.append(tag_obj)

            new_blog.tags.set(tag_objs)
            form.save_m2m()  
            messages.success(request, "Blog saved successfully!")
            return redirect('BlogDetail', blog_id=new_blog.id)
    else:
        initial = {}
        if blog:
            initial['tags_input'] = ', '.join([t.name for t in blog.tags.all()])
        form = BlogPostForm(instance=blog, initial=initial)
    return render(request, 'CreateEditBlog.html', {'form': form, 'blog': blog})

@csrf_exempt
def add_comment(request, blog_id):
    if request.method == "POST" and request.user.is_authenticated:
        blog = get_object_or_404(BlogPost, id=blog_id)
        data = json.loads(request.body)
        content = data.get("content", "")
        if content:
            comment = Comment.objects.create(post=blog, author=request.user, content=content)
            return JsonResponse({"success": True, "author": comment.author.username, "content": comment.content})
    return JsonResponse({"success": False})


@csrf_exempt
def toggle_like(request, blog_id):
    if request.method == "POST" and request.user.is_authenticated:
        blog = get_object_or_404(BlogPost, id=blog_id)
        like, created = Like.objects.get_or_create(post=blog, user=request.user)
        if not created:
            like.delete()
            liked = False
        else:
            liked = True
        return JsonResponse({"liked": liked, "total_likes": blog.likes.count()})
    return JsonResponse({"liked": False, "total_likes": 0})


def DeleteBlog(request, blog_id):
    blog = get_object_or_404(BlogPost, id=blog_id)
    if request.user != blog.author:
        messages.error(request, "You are not allowed to delete this blog.")
        return redirect('BlogDetail', blog_id=blog.id)
    if request.method == 'POST':
        blog.delete()
        messages.success(request, "Blog deleted successfully!")
        return redirect('HomePage')
    return render(request, 'ConfirmDelete.html', {'blog': blog})


def blog_tldr(request, blog_id):
    blog = get_object_or_404(BlogPost, id=blog_id)
    try:
        summary = summarizer(blog.content, max_length=100, min_length=30, do_sample=False)[0]['summary_text']
    except:
        words = blog.content.split()
        summary = " ".join(words[:150]) + ("..." if len(words) > 150 else "")
    return JsonResponse({"summary": summary})


@login_required
def my_blogs(request):
    user_blogs = BlogPost.objects.filter(author=request.user).order_by('-created_at')
    return render(request, "MyBlogs.html", {"blogs": user_blogs})

def register_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f"Account created for {user.username}! You can now log in.")
            return redirect('login')
        messages.error(request, "Please correct the errors below.")
    else:
        form = CustomUserCreationForm()
    return render(request, "register.html", {"form": form})

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect('HomePage')
    else:
        form = AuthenticationForm()
    return render(request, "login.html", {"form": form})

def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('HomePage')
