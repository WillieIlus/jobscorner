from __future__ import unicode_literals

from builtins import super

import np
import numpy as np
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from taggit.managers import TaggableManager
from taggit.models import TaggedItemBase

from accounts.models import User
from blog.models import STATUS_CHOICES
from category.models import Category
from location.models import Location


class TaggedCompany(TaggedItemBase):
    content_object = models.ForeignKey('Company', on_delete=models.PROTECT)


class PublishedManager(models.Manager):

    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status='published')


class Company(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    name = models.CharField(max_length=120, help_text='Name of your company', )
    slug = models.SlugField(unique=True, blank=True, null=True)
    logo = models.ImageField(upload_to="logos/company", blank=True, null=True)
    image = models.ImageField(upload_to="mainimage/company", blank=True, null=True)
    description = models.TextField(max_length=1024)
    category = models.ForeignKey(Category, related_name="company", blank=True, null=True, on_delete=models.PROTECT)
    website = models.URLField(blank=True, null=True, help_text="Please leave empty if none")
    twitter = models.CharField(max_length=20, blank=True, help_text="Please leave empty if none")
    location = models.ForeignKey(Location, related_name='company', blank=True, null=True,
                                 help_text="Please leave empty if 100% virtual",
                                 on_delete=models.PROTECT)
    email = models.EmailField(blank=True, null=True, help_text="Please leave empty if none")
    address = models.CharField(max_length=255, blank=True, )

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="draft")
    tags = TaggableManager(through=TaggedCompany)

    publish = models.DateTimeField('date published', auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)

    objects = models.Manager()
    published = PublishedManager()

    class Meta:
        ordering = ('name',)
        verbose_name_plural = "companies"

    _metadata = {
        'title': 'name',
        'description': 'description',
        'image': 'get_meta_image',
    }

    def get_meta_image(self):
        if self.image:
            return self.image.url

    def average_rating(self):
        all_ratings = list(map(lambda x: x.rating, self.review_set.all()))
        return np.mean(all_ratings)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        slug = slugify(self.name)
        self.slug = slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('company:detail', kwargs={'slug': self.slug})


class CompanyImage(models.Model):
    img = models.ImageField(upload_to='company/company_photos', null=True)
    alt = models.CharField(max_length=256, null=True, default="")
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='photos')

    def __str__(self):
        return "{}: {}".format(self.company.name, self.img.url)


WEEKDAYS = [
    (1, "Monday"),
    (2, "Tuesday"),
    (3, "Wednesday"),
    (4, "Thursday"),
    (5, "Friday"),
    (6, "Saturday"),
    (7, "Sunday"),
]


class OpeningHours(models.Model):
    """
    Store opening times of company premises,
    defined on a daily basis (per day) using one or more
    start and end times of opening slots.
    """
    company = models.ForeignKey(Company, verbose_name='Company', related_name='open_hours', on_delete=models.CASCADE)
    slug = models.SlugField(max_length=50, unique=True)
    weekday = models.IntegerField('Weekday', choices=WEEKDAYS)
    from_hour = models.TimeField('Opening')
    to_hour = models.TimeField('Closing')

    class Meta:
        verbose_name = 'Opening Hours'
        verbose_name_plural = 'Opening Hours'
        ordering = ['company', 'weekday', 'from_hour']

    def __str__(self):
        return "%(company)s %(weekday)s (%(from_hour)s - %(to_hour)s)" % {
            'company': self.company,
            'weekday': self.weekday,
            'from_hour': self.from_hour,
            'to_hour': self.to_hour
        }

    def save(self, *args, **kwargs):
        # slug = slugify(("%s + %s" %self.company.name, %weekday))
        # slug = slugify(self.company.name)
        slug = slugify("%s - %s" % (self.company.name, self.weekday))
        self.slug = slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('company:detail', kwargs={"slug": self.company.slug})


class ClosingRules(models.Model):
    """
    Used to overrule the OpeningHours. This will "close" the store due to
    public holiday, annual closing or private party, etc.
    """

    class Meta:
        verbose_name = 'Closing Rule'
        verbose_name_plural = 'Closing Rules'
        ordering = ['start']

    company = models.ForeignKey(Company, verbose_name='Company', on_delete=models.CASCADE)
    start = models.DateTimeField('Start')
    end = models.DateTimeField('End')
    reason = models.TextField('Reason', null=True, blank=True)

    def __str__(self):
        return "%(premises)s is closed from %(start)s to %(end)s due to %(reason)s" % {
            'premises': self.company.name,
            'start': str(self.start),
            'end': str(self.end),
            'reason': self.reason
        }

    def get_absolute_url(self):
        return reverse('company:detail', kwargs={"slug": self.company.slug})
