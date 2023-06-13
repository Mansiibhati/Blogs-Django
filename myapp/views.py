from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Post
from .forms import PostForm
from django.utils import timezone

#decorator that ensures that user must be authenticated
@login_required
#a function that takes request
def create_post(request):
    #checks if the request method is POST,if POST
    if request.method == 'POST':
        #create a form instance based on PostForm class using data from request.POST dict
        form = PostForm(request.POST)
        #check if form is valid
        if form.is_valid():
            #if valid save form in post variable
            post = form.save(commit=False)
            #assigns the currently loged in user request.user as author of post
            post.author = request.user
            #if user selects publish
            if 'publish' in request.POST:
                #sets the published date to current date & time
                post.published_date = timezone.now()
                #sets the status field of the post object to published
                post.status = 'published'
            #saves the post object to database
            post.save()
            #redirect to post detail url
            return redirect('post_detail', pk=post.pk)
    else:
        #if method is not POST a new empty form is created using PostForm()
        form = PostForm()
        #render create_post.html template with form as context data
    return render(request, 'create_post.html', {'form':form})

@login_required
def update_post(request,pk):
    #retrieve an obj from db based on pk or raise an error
    post = get_object_or_404(Post,pk=pk)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            if 'save_draft' in request.POST:    # Check if "Save as Draft" button was clicked
                post.published_date = timezone.now()
                post.status = 'draft'
            elif 'publish' in request.POST:
                post.published_date = timezone.now()
                post.status = 'published'
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
        return render(request, 'update_post.html', {'form':form})
    
def post_detail(request, pk):
    '''this function will show the detail of a specific post'''
    post = get_object_or_404(Post,pk=pk)
    return render(request, 'post_detail.html', {'post': post})

def home(request):
    '''this function is for home page public page '''
    if request.user.is_authenticated:
        posts = Post.objects.all()
    else:
        posts = Post.objects.filter(status = 'published')

    return render(request, 'home.html',{'posts': posts})

def delete_post(request, post_id):
    '''this will allow the user to delete a post'''
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        post.delete()
        return redirect('home')
    else:
        return render(request, 'delete_post.html', {'post': post})
    



    







