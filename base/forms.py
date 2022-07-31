from django.forms import ModelForm
from django import forms
from base.models import Blog

class BlogForm(ModelForm):
    class Meta:
        model = Blog
        fields = '__all__'
        exclude = ['author']
    

# class BlogImageForm(ModelForm):
#     class Meta:
#         model = Blog
#         fields = ['blog_image']

