from __future__ import unicode_literals

from builtins import super

from django.db import models
from django.urls import reverse
from django.utils.text import slugify

from country.models import Country


class Location(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=200, blank=True, null=True)
    photo = models.ImageField(upload_to="address/location", blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    country = models.ForeignKey(Country, related_name='country', on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "locations"
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        slug = slugify(self.name)
        self.slug = slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("location:detail", kwargs={"slug": self.slug})
