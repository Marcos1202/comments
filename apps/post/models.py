from django.db import models
from django.db.models.signals import pre_save
from django.conf import settings
from django.utils.text import slugify


# Create your models here.
class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField(max_length=260, blank=True, null=True)
    slug = models.SlugField(unique=True, blank=True)
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text

def new_url(instance, url=None):
    slug = slugify(instance.text)
    if url is not None:
        slug = url

    qs = Post.objects.filter(slug=slug).order_by("-id") 
    if qs.exists():
        new_url_si = "%s-%s"%(slug, qs.first().id)
        return new_url(instance, url=new_url_si)
    return slug

def create_url(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = new_url(instance)

pre_save.connect(create_url, sender=Post)