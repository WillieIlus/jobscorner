from __future__ import unicode_literals

from builtins import super

import numpy as np
import np
from django.db import models
from django.urls import reverse
from django.utils.text import slugify

from taggit.managers import TaggableManager

from accounts.models import User
from category.models import Category
from location.models import Location

WEEK_DAYS = (
    ('Monday', 'Monday'),
    ('Tuesday', 'Tuesday'),
    ('Wednesday', 'Wednesday'),
    ('Thursday', 'Thursday'),
    ('Friday', 'Friday'),
    ('Saturday', 'Saturday'),
    ('Sunday', 'Sunday'),
)


class Company(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    name = models.CharField(max_length=120, help_text='Name of your company', )
    slug = models.SlugField(unique=True, blank=True, null=True)
    logo = models.ImageField(upload_to="logos/company", blank=True, null=True)
    description = models.TextField(max_length=1024)
    category = models.ForeignKey(Category, blank=True, null=True, on_delete=models.PROTECT)
    website = models.URLField(blank=True, null=True, help_text="Please leave empty if none")
    twitter = models.CharField(max_length=20, blank=True,  help_text="Please leave empty if none")
    location = models.ForeignKey(Location, blank=True, null=True, help_text="Please leave empty if 100% virtual",
                                 on_delete=models.PROTECT)
    email = models.EmailField(blank=True, null=True, help_text="Please leave empty if none")
    address = models.CharField(max_length=255, blank=True, )
    openTime = models.TimeField(blank=True, null=True, )
    closeTime = models.TimeField(blank=True, null=True, )
    openDays = models.CharField(max_length=10, choices=WEEK_DAYS, verbose_name="Open Days")
    closeDays = models.CharField(max_length=10, choices=WEEK_DAYS, verbose_name="Close Days")
    tags = TaggableManager()

    class Meta:
        ordering = ('name',)
        verbose_name_plural = "companies"

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
