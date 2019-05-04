from accounts.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from location.models import Location
from taggit.managers import TaggableManager
from taggit.models import TaggedItemBase


class TaggedProfile(TaggedItemBase):
    content_object = models.ForeignKey('Profile', on_delete=models.PROTECT)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='profile')
    title = models.CharField(max_length=100, blank=True)
    slug = models.SlugField(max_length=200, blank=True, null=True, unique=True)
    bio = models.TextField(max_length=500, blank=True)
    location = models.ForeignKey(Location, related_name='profile', blank=True, null=True, on_delete=models.PROTECT)
    birth_date = models.DateField(null=True, blank=True)
    thumbnail = models.ImageField(upload_to="users/thumbnail", blank=True, null=True)
    phone = models.IntegerField(blank=True, null=True)
    website = models.URLField(max_length=300, blank=True, null=True)
    facebook = models.CharField(max_length=100, blank=True)
    instagram = models.CharField(max_length=100, blank=True)
    twitter = models.CharField(max_length=100, blank=True)
    linkedin = models.CharField(max_length=100, blank=True)
    google = models.CharField(max_length=100, blank=True)
    pinterest = models.CharField(max_length=100, blank=True)
    tags = TaggableManager(through=TaggedProfile)

    publish = models.DateTimeField('date published', auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)

    def save(self, *args, **kwargs):
        slug = slugify(self.user.username)
        self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        return reverse('resume:detail', kwargs={"slug": self.slug})


SKILL_LEVELS = (
    (None, 'unknown'),
    ('B', 'beginner'),
    ('S', 'skilled'),
    ('A', 'advanced'),
    ('E', 'expert'),
)


class Skill(models.Model):
    profile = models.ForeignKey(Profile, related_name="skills", on_delete=models.CASCADE)
    name = models.CharField(max_length=200, unique=True, verbose_name="name")
    description = models.TextField(max_length=2000, blank=True)
    level = models.CharField(max_length=1, choices=SKILL_LEVELS, verbose_name="level")
    tags = TaggableManager()

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('resume:detail', kwargs={"slug": self.profile.slug})


class Experience(models.Model):
    profile = models.ForeignKey(Profile, related_name='experience', on_delete=models.CASCADE)
    role = models.CharField(max_length=150)
    company = models.CharField(max_length=150)
    company_url = models.URLField('Company URL')
    start_date = models.DateField(null=True, blank=True, verbose_name="start date")
    completion_date = models.DateField(null=True, blank=True, verbose_name="end date")
    description = models.TextField(verbose_name="description")
    is_current = models.BooleanField(default=True, verbose_name="still in office")

    class Meta:
        ordering = ['-completion_date', '-start_date']

    def clean(self):
        if self.start_date and self.completion_date:
            if self.start_date > self.completion_date:
                raise ValidationError({"start_date": ("Start date must be "
                                                      "before end date."),
                                       "completion_date": ("Start date must be "
                                                           "before end date.")})

    def get_absolute_url(self):
        return reverse('resume:detail', kwargs={"slug": self.profile.slug})


class Education(models.Model):
    profile = models.ForeignKey(Profile, related_name='education', on_delete=models.CASCADE)
    school = models.CharField(max_length=150, verbose_name="school")
    school_url = models.URLField('School URL')
    major = models.CharField(max_length=50, blank=True, )
    result = models.CharField(max_length=150, blank=True, verbose_name="result")
    start_date = models.DateField(null=True, blank=True, verbose_name="start date")
    completion_date = models.DateField(null=True, blank=True, verbose_name="end date")
    summary = models.TextField(max_length=3000, blank=True, verbose_name="Summary description")
    is_current = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Education"

    def __str__(self):
        return self.major

    def clean(self):
        if self.start_date and self.completion_date:
            if self.start_date > self.completion_date:
                raise ValidationError({"start_date": ("Start date must be "
                                                      "before end date."),
                                       "completion_date": ("Start date must be "
                                                           "before end date.")})

    def get_absolute_url(self):
        return reverse('resume:detail', kwargs={"slug": self.profile.slug})
