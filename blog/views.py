from django.shortcuts import render, get_object_or_404, redirect
from blog.models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from blog.forms import CommentForm, BlogForm
from taggit.models import Tag
from django.db.models import Count, Q 



def post_list(request, tag_slug=None):
    context = {}    
    posts = Post.published.all()#using custom manager    
    paginator = Paginator(posts, 2)
    page = request.GET.get('page')
    
    
    
    
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        posts=posts.filter(tags__in=[tag])
        
    query = request.GET.get("q")
    if query:
        posts=Post.published.filter(Q(title__icontains=query) | Q(tags__name__icontains=query)).distinct()
    
    
    try:
        posts = paginator.page(page)
    except PageNotAnInteger :
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
        
    
    blog_post = BlogForm(request.POST or None)
    if blog_post.is_valid():        
        
        blog_post.save()
        return redirect('/')
    else:
        blog_post = BlogForm()
        
        
        
         
    context['blog_post']= blog_post
    # context['blog_post_author']= author
    
    
    context['posts'] = posts
    context['pages'] = page          
    return render(request, 'post_list.html', context)

def post_detail(request, post):    
    post = get_object_or_404(Post, slug=post, status='published')
    
    text = {
        'add_comment': 'AddComments',
        'ccomment': 'Comment',
        'no_comments' : 'No Comment Yet!!'
    }
    
    
    comments = post.comments.filter(active = True)
    new_comment = None
    
    if request.method == 'POST':
        
        comment_form = CommentForm(data=request.POST)
        
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
            return redirect(post.get_absolute_url() + '#' + str(new_comment.id))
        else:
            comment_form = CommentForm() 
    else:
        comment_form = CommentForm() 
        
    post_tags_id = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(tags__in = post_tags_id).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags = Count('tags')).order_by('-same_tags', '-publish')[:6]
              
    
    return render(request, 'post_detail.html',{'post':post,'comments': comments,'comment_form':comment_form, 'text': text, 'similar_posts':similar_posts})

def reply_page(request):
    if request.method == 'POST':
        form =CommentForm(request.POST)
        if form.is_valid():
            post_id = request.POST.get('post_id')
            parent_id = request.POST.get('parent')
            post_url = request.POST.get('post_url')
            
            reply = form.save(commit=False)   
                     
            reply.post = Post(id=post_id)            
            reply.parent = Comment(id=parent_id)
            reply.save()
            
            return redirect(post_url+'#'+str(reply.id))
    return redirect('/')
    
