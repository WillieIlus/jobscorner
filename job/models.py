from __future__ import unicode_literals

from accounts.models import User
from actstream import registry
from category.models import Category
from company.models import Company
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from location.models import Location
from taggit.managers import TaggableManager
from taggit.models import TaggedItemBase


class TaggedJob(TaggedItemBase):
    content_object = models.ForeignKey('Job', on_delete=models.PROTECT)


class Job(models.Model):
    user = models.ForeignKey(User, blank=True, null=True, related_name="job", on_delete=models.PROTECT)
    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, unique=True)
    salary = models.CharField(max_length=128, blank=True)
    description = models.TextField(help_text="qualification, responsibilities,  requirements,  benefits, Experience")
    application_info = models.TextField(help_text="What's the best way to apply for this job?")
    work_hours = models.CharField(max_length=80, blank=True)
    url = models.CharField(max_length=1024, blank=True)
    contact_email = models.EmailField(max_length=254, blank=True, null=True, )
    location = models.ForeignKey(Location, related_name='job', blank=True, null=True, on_delete=models.PROTECT)
    category = models.ForeignKey(Category, related_name='job', on_delete=models.PROTECT)
    company = models.ForeignKey(Company, on_delete=models.PROTECT)
    opening = models.IntegerField(default=1, blank=True, null=True)
    remote = models.BooleanField(default=False, help_text="Select if this job allows 100% remote working")
    tags = TaggableManager(through=TaggedJob)

    publish = models.DateTimeField('date published', auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return self.title

    _metadata = {
        'title': 'title',
        'description': 'description',
    }


    def save(self, *args, **kwargs):
        slug = slugify(self.title)
        self.slug = slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('job:detail', kwargs={"slug": self.slug})
