from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from autoslug import AutoSlugField
from django.urls import reverse
from ckeditor_uploader.fields import RichTextUploadingField
from taggit.managers import TaggableManager



#creating custom manager
class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status='published')

class Post(models.Model):
    STATUS_CHOICE = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    
    title = models.CharField(max_length=250)
    image = models.ImageField(upload_to='featured_image/%Y/%m/%d/') 
    slug = AutoSlugField(populate_from='title', unique = True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    body = RichTextUploadingField()
    
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    status = models.CharField(max_length=10, choices=STATUS_CHOICE, default='draft')
    
    tags = TaggableManager() 
    
    class Meta:
        ordering = ('-publish',)        
    def __str__(self) -> str:
        return self.title
        
    objects = models.Manager()#default manager
    published = PublishedManager()#Cutom Manager
    
    def get_absolute_url(self):
        return reverse('blog:post_detail', args=[self.slug])
    def get_comments(self):
        return self.comments.filter(parent=None).filter(active=True)
    
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name = 'comments')
    name =models.CharField(max_length=50)
    email = models.EmailField()
    parent = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True)
    body = models.TextField()
    
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    
    
    
    
    
    class Meta:
        ordering = ('created',)        
    def __str__(self):
        return self.body
        
    def get_comments(self):
        return Comment.objects.filter(parent=self).filter(active=True)
        
