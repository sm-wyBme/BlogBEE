from django.shortcuts import render, redirect
from base.models import Blog, Comment, Topic
from account.models import Account
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from base.forms import BlogForm
from django.db.models import Q

# Create your views here.

#home view
def home_view(request, *args, **kwargs):

    q = request.GET.get('q') if request.GET.get('q') != None else ''
    blogs = Blog.objects.filter( 
        Q(topic__name__icontains=q)|
        Q(title__icontains=q) |
        Q(author__name__icontains=q) |
        Q(author__username__icontains=q)
    )

    topics = Topic.objects.all()
    blogs = Blog.objects.all()
    context = {
        'blogs' : blogs,
        'topics' : topics,
    }
    
    return render(request, 'base/home.html', context)

#blog view
def blog_view(request, *args, **kwargs):

    blog_id = kwargs.pop('blog_id')
    try:
        blog = Blog.objects.get(id=blog_id)
    except Blog.DoesNotExist:
        return HttpResponse("Blog does not exist")
    
    blog_comments = blog.comment_set.all() #all the comments on the blog
    other_blogs = blog.author.blog_set.all() 
    context = {
        'blog': blog,
        'other_blogs': other_blogs,
        'blog_comments': blog_comments,
    }

    if request.method == 'POST':
        comments = Comment.objects.create(
            author = request.user,
            blog = blog,
            body = request.POST.get('body')
        )
        return redirect('base:blog', blog.id)

    return render(request, 'base/blog.html', context)

#create blog
@login_required(login_url='login')
def create_blog(request, *args, **kwargs):

    # form = BlogForm()
    topics = Topic.objects.all()
    form = BlogForm()

    if request.POST:
        
        if form.is_valid():
            form.save()
        # blog_topic = form.cleaned_data['topic']
        blog_topic = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name = blog_topic)

        blog = Blog.objects.create(
            author=request.user,
            topic = topic,
            title = request.POST.get('title'),
            body = request.POST.get('body'),
        )
        
        return redirect('base:blog', blog.id)

    context = {'form': form, 'topics': topics}
    return render(request, 'base/create-blog.html', context)

#update a blog
@login_required(login_url='login')
def update_blog(request, pk):
    try:
        blog = Blog.objects.get(id = pk)
    except Blog.DoesNotExist:
        return HttpResponse("Blog does not exist")
    
    if request.user != blog.author:
        context = {
                'message': "You are not allowed to edit this blog",
            }
        return render(request, 'message.html', context)
        
    form = BlogForm(instance=blog) #prefilled
    topics = Topic.objects.all()

    if request.method == 'POST':
        blog_topic =  request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name = blog_topic)
        blog.topic = topic
        blog.title = request.POST.get('title')
        blog.body = request.POST.get('body')
        if len(request.FILES) > 0:
            blog.blog_image = request.FILES['image']
        blog.save()
        # return redirect('base:blog', blog.id)
        return redirect('account:view', user_id=request.user.id)

    context = {'form': form, 'blog': blog}
    return render(request, 'base/create-blog.html', context)

#update blog image
# @login_required(login_url='login')
# def update_blog_image(request, pk):
#     try:
#         blog = Blog.objects.get(id = pk)
#     except Blog.DoesNotExist:
#         context = {
#                 'message': "Blog does not exist",
#         }
#         return render(request, 'message.html', context)
    
#     if request.user != blog.author:
#         context = {
#             'message': "You are not allowed to edit this blog",
#         }
#         return render(request, 'message.html', context)

#     imageForm = BlogImageForm(instance = blog)
    
#     if request.method == 'POST':

#         imageForm = BlogImageForm(request.POST, request.FILES, instance = blog)
#         if len(request.FILES) > 0:
#             blog.blog_image = request.FILES['image']
#             blog.save()
#         # if imageForm.is_valid():
#         #     imageForm.save()
#             return redirect('base:blog', blog.id)
#         else:
#             imageForm = BlogImageForm(instance = blog)
            
#     context = {'imageForm': imageForm, 'blog': blog}
#     return render(request, 'base/update-blog-image.html', context)

#delete blog
@login_required(login_url='login')
def delete_blog(request, pk):
    try:
        blog = Blog.objects.get(id=pk)
    except Blog.DoesNotExist:
        return HttpResponse("Blog does not exist")
    if(request.user != blog.author):
        context = {
            'message': "You are not allowed to delete this blog",
        }
        return render(request, 'message.html', context)

    if request.POST:
        blog.delete()
        return redirect('account:view', request.user.id)

    context = {
        'obj' : blog
    }
    return render(request, 'base/delete.html', context)

#delete a comment
@login_required(login_url = 'login')
def delete_comment(request, pk):
    try:
        comment = Comment.objects.get(id=pk)
    except Comment.DoesNotExist:
        return HttpResponse("Comment does not exist")
    
    if(request.user != comment.author):
        context = {
            'message': "You are not allowed to delete this comment",
        }
        return render(request, 'message.html', context)

    if request.POST:
        comment.delete()
        return redirect('base:blog', comment.blog.id)

    context = {
        'obj' : comment
    }
    return render(request, 'base/delete.html', context)

