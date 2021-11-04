from django import forms
from django.forms import fields
from .models import *
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')
    
    # overriding default form setting and adding bootstrap class
    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs = {'placeholder': 'Enter name','class':'form-control'}
        self.fields['email'].widget.attrs = {'placeholder': 'Enter email', 'class':'form-control'}
        self.fields['body'].widget.attrs = {'placeholder': 'Comment here...', 'class':'form-control', 'rows':'5'}
        
class BlogForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = '__all__' 
        # fields = [
        #     "title",
        #     "image",
        #     "author",
        #     "body",
        #     "tags",
        #     "status",
        # ]