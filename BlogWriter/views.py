from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from .models import BlogPost, Tag
from .forms import CustomUserCreationForm, BlogPostForm
from transformers import pipeline


# ---------------- Home Page ----------------
def HomePage(request):
    blogs = BlogPost.objects.all().order_by('-created_at')
    return render(request, "HomePage.html", {"blogs": blogs})

# ---------------- Blog Detail ----------------
def BlogDetail(request, blog_id):
    blog = get_object_or_404(BlogPost, id=blog_id)
    related_blogs = []
    first_tag = blog.tags.first()
    if first_tag:
        related_blogs = first_tag.posts.exclude(id=blog.id)[:3]
    return render(request, "BlogDetail.html", {
        "blog": blog,
        "related_blogs": related_blogs
    })

# ---------------- Create/Edit Blog ----------------
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
            form.save_m2m()  # save tags
            messages.success(request, "Blog saved successfully!")
            return redirect('BlogDetail', blog_id=new_blog.id)
    else:
        form = BlogPostForm(instance=blog)

    return render(request, 'CreateEditBlog.html', {'form': form, 'blog': blog})

# ---------------- Delete Blog ----------------
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

summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def blog_tldr(request, blog_id):
    blog = get_object_or_404(BlogPost, id=blog_id)
    try:
        summary_result = summarizer(blog.content, max_length=100, min_length=30, do_sample=False)
        summary = summary_result[0]['summary_text']
    except Exception as e:
        # fallback
        words = blog.content.split()
        summary = " ".join(words[:50]) + ("..." if len(words) > 50 else "")
    
    return JsonResponse({"summary": summary})
# ---------------- Register ----------------
def register_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f"Account created for {user.username}! You can now log in.")
            return redirect('login')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = CustomUserCreationForm()
    return render(request, "register.html", {"form": form})

# ---------------- Login ----------------
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

# ---------------- Logout ----------------
def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('HomePage')
