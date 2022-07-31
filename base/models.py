from django.db import models
from tinymce.models import HTMLField
from account.models import Account
from PIL import Image
from django.conf import settings
import os

#image for blog
def get_blog_image_filepath(self, filename):
    blog_image_name = f'blog_images/{self.pk}/{"blog_image.png"}'
    full_path = os.path.join(settings.MEDIA_ROOT, blog_image_name)

    if os.path.exists(full_path):
        os.remove(full_path)

    return blog_image_name

def get_default_blog_image_filepath():
    return 'custom_images/dummy_blog_image.jpg'

#topic model
class Topic(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)
    
    def __str__(self):
        return self.name


#blog model
class Blog(models.Model):

    author              = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True)
    title               = models.CharField(max_length=200)
    topic               = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    body                = HTMLField()
    updated             = models.DateTimeField(auto_now=True) #last updated
    created             = models.DateTimeField(auto_now_add=True) #created DateTimeField
    # blog_image       = models.ImageField(max_length=255, upload_to=get_blog_image_filepath, null=True, blank=True, default=get_default_blog_filepath)
    # blog_image          = models.ImageField(max_length=255, upload_to=get_blog_image_filepath, null=True, blank=True, default=get_default_blog_image_filepath)

    class Meta:
        ordering = ['-created']
    
    def summary(self):
        return self.body[:50]
    
    #crop before save
    # def save(self, *args, **kwargs):
    #     super().save(*args, **kwargs)

    #     SIZE = 800, 450

    #     if self.blog_image:
    #         picture = Image.open(self.blog_image.path)
    #         picture.thumbnail(SIZE, Image.LANCZOS)
    #         picture.save(self.blog_image.path)



    #get the file name uploaded by the user and change the name of the file to the generic name
    def get_blog_image_filename(self):
        return str(self.blog_image)[str(self.blog_image).index(f'blog_images/{self.pk}/'):]

    def __str__(self):
        return self.title


#comment of the blog
class Comment(models.Model):

    author                = models.ForeignKey(Account, on_delete=models.CASCADE)
    blog                  = models.ForeignKey(Blog, on_delete=models.CASCADE)
    body                  = models.TextField()
    updated               = models.DateTimeField(auto_now=True)
    created               = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.body
