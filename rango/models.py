from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from datetime import datetime


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=128, unique=True)
    view = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        if self.view < 0:
            self.view = 0
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name

class Page(models.Model):
    category = models.ForeignKey(Category)
    title = models.CharField(max_length=128)
    url = models.URLField()
    views = models.IntegerField(default=0)
    first_visit = models.DateTimeField(default=None)
    last_visit = models.DateTimeField(default=None)

    def save(self, *args, **kwargs):
        if self.first_visit > datetime.now():
            self.first_visit = datetime.now()
        if self.last_visit > datetime.now():
            self.last_visit = datetime.now()
        if self.first_visit > self.last_visit:
            self.last_visit = self.first_visit
        super(Page, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.title

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    website = models.URLField(blank=True)
    picture = models.ImageField(upload_to='profile_images', blank=True)

    def __unicode__(self):
        return self.user.username

