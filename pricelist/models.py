from __future__ import unicode_literals

from builtins import super

import numpy as np
from django.db import models
from django.urls import reverse
from django.utils.text import slugify

# what this moddule does is displaying the price median price, minunum and maximum price and displaying the companies that offer the services
# it goes this way a model to display the activity and the prices
# what is the price of printing and a banner 1 meter squared on roland
# or what is the price of printing a banner 1 meter squared on flora
# what is the price of hosting a meeting for and hour in a hotel
# what is the price of repairing a phone nokia
from accounts.models import User
from company.models import Company
from location.models import Location


class PublishedManager(models.Manager):

    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status='published')


STATUS_CHOICES = (
    ('draft', 'Draft'),
    ('published', 'Published'),
)

NEGOTIABLE = (
    ('yes', 'Yes'),
    ('no', 'No'),
)


class Type(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, blank=True, null=True, unique=True)

    class Meta:
        verbose_name_plural = "types"
        ordering = ['name']

    _metadata = {
        'title': 'name',
    }

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        slug = slugify(self.name)
        self.slug = slug
        super().save(*args, **kwargs)


class Item(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, blank=True, null=True, unique=True)
    type = models.ForeignKey(Type, related_name='item', on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "items"
        ordering = ['name']

    _metadata = {
        'title': 'name',
    }

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        slug = slugify(self.name)
        self.slug = slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('item:detail', kwargs={'slug': self.slug})


class Service(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, blank=True, null=True, unique=True)
    description = models.TextField(blank=True, null=True)
    item = models.ForeignKey(Item, related_name='service', on_delete=models.CASCADE)
    type = models.ForeignKey(Type, related_name='service', blank=True, null=True, on_delete=models.PROTECT)
    location = models.ForeignKey(Location, related_name='service', blank=True, null=True, on_delete=models.PROTECT)

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="draft")
    publish = models.DateTimeField('date published', auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    objects = models.Manager()
    published = PublishedManager()

    class Meta:
        verbose_name_plural = "services"
        ordering = ['name', 'publish']

    _metadata = {
        'title': 'name',
        'description': 'description',
    }

    def __str__(self):
        return "The price of %s a %s %s is" % (self.name, self.type, self.item)

    def average_price(self):
        all_prices = list(map(lambda x: x.amount, self.service.all()))
        return np.mean(all_prices)

    def save(self, *args, **kwargs):
        pricequestion = "The Price of %s %s %s" %(self.name, self.type, self.item)
        slug = slugify(pricequestion)
        self.slug = slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('pricelist:detail', kwargs={'slug': self.slug})


class Price(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.FloatField()
    service = models.ForeignKey(Service, related_name='service', on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to="pricelist/item", blank=True, null=True)
    company = models.ForeignKey(Company, blank=True, null=True, on_delete=models.PROTECT)

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="draft")
    negotiable = models.CharField(max_length=10, choices=NEGOTIABLE, default="yes")
    publish = models.DateTimeField('date published', auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    objects = models.Manager()
    published = PublishedManager()

    class Meta:
        verbose_name_plural = "prices"
        ordering = ['amount', 'publish']
        unique_together = ('service', 'user')

    def __str__(self):
        return "%s" % (self.amount,)
