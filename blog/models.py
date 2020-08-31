from django.db import models
from django.urls import reverse
from django.db.models.signals import pre_save
from django.utils.text import slugify
from django.conf import settings
from django.utils import timezone
# Create your models here.


class Posterman(models.Manager):
    def active(self, *args, **kwargs):
        return super(Posterman, self).filter(draft = False).filter(published__lte = timezone.now())


def upload_location(instance, filename):
    return "%s/%s" %(instance.id, filename)
    # filebase, extension = filename.split(".")
    # return "%s/%s.%s" %(instance.id, instance.id, extension)

class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, on_delete = models.SET_NULL, null= True)
    title = models.CharField(max_length=30)
    slug = models.SlugField(unique= True)
    photu = models.ImageField(null = True, upload_to= upload_location, 
            width_field= "wd",
            height_field= "ht")
    ht = models.IntegerField(default=0)
    wd = models.IntegerField(default=0)
    content = models.TextField()
    draft = models.BooleanField(default=False)
    published = models.DateTimeField()
    updated = models.DateTimeField(auto_now=True)
    made = models.DateTimeField(auto_now_add= True)

    objects = Posterman()
    # posts = Posterman() then we can use Post.posts.all()/.get()

    def __str__(self):
        return self.title

    def url(self):
        return reverse("posts:detail", kwargs={"slug": self.slug})

    class Meta:
        ordering = [ '-updated']



def creslug(instance,new_slug = None):
    slug = slugify(instance.title)
    if new_slug is not None:
        slug = new_slug
    qs = Post.objects.filter(slug = slug).order_by("-id")
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" %(slug, qs.first().id)
        return creslug(instance, new_slug= new_slug)
    return slug


def post_incoming(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = creslug(instance)




pre_save.connect(post_incoming, sender = Post)