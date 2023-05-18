from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Post
from .forms import PostForm
from django.utils import timezone

@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            if 'publish' in request.POST:
                post.published_date = timezone.now()
                post.status = 'published'
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'create_post', {'form':form})

@login_required
def update_post(request,pk):
    post = get_object_or_404(Post,pk=pk)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            if 'save_draft' in request.POST:    # Check if "Save as Draft" button was clicked
                print("i am here ")
                post.published_date = timezone.now()
                post.status = 'draft'
            elif 'publish' in request.POST:
                print('i am in elif ')
                post.published_date = timezone.now()
                post.status = 'published'
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
        return render(request, 'update_post', {'form':form})
    
def post_detail(request, pk):
    post = get_object_or_404(Post,pk=pk)
    return render(request, 'post_detail', {'post': post})

def home(request):
    if request.user.is_authenticated:
        posts = Post.objects.all()
    else:
        posts = Post.objects.filter(status = 'published')

    return render(request, 'home',{'posts': posts})

def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        post.delete()
        return redirect('home')
    else:
        return render(request, 'delete_post', {'post': post})
    



    







