from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .forms import BlogPostForm
from django.contrib.auth.decorators import login_required
from .forms import Register, Login
from .models import BlogPost
from django.shortcuts import render, get_object_or_404
def home(request):
    return render(request,'home.html')
def signup(request):
    if request.method=='POST':
        form=Register(request.POST)
        if form.is_valid():
            username=form.cleaned_data['username']
            email=form.cleaned_data['email']
            password=form.cleaned_data['password']
            if User.objects.filter(username=username).exists():
                messages.error(request, "This username is already taken. Please choose a different one.")
                return redirect('signup')
            User.objects.create_user(username=username,email=email,password=password)
            messages.success(request,'sign-up successful! please sign in')
            return redirect('signin')
    else:
        form=Register()
    return render(request,'signup.html',{'form':form})
def signin(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('blog') 
        else:
            messages.error(request, "Invalid username or password")
            return render(request, "signin.html")
    return render(request, "signin.html")
def blog(request):
    query = request.GET.get('q', '')
    if query:
        posts = BlogPost.objects.filter(title__icontains=query)
    else:
        posts = BlogPost.objects.all()
    return render(request,'blog.html',{'posts':posts})
@login_required
def write_blog(request):
    if request.method == "POST":
        form = BlogPostForm(request.POST)
        if form.is_valid():
            blog_post = form.save(commit=False)
            blog_post.author = request.user  
            blog_post.save()
            return redirect('blog')  
    else:
        form = BlogPostForm()
    
    return render(request, 'write_blog.html', {'form': form})
def logout(request):
    return render(request,'logout.html')
def profile(request):
    return render(request,'profile.html')
def user_logout(request):
    logout(request)
    return redirect('home')
def post_detail(request, post_id):
    post = get_object_or_404(BlogPost, id=post_id)
    return render(request, 'post_detail.html', {'post': post})
@login_required
def delete_blog(request, post_id):
    post = get_object_or_404(BlogPost, id=post_id)
    if post.author == request.user:
        post.delete()
        return redirect('blog')
    else:
        return redirect('blog')