from django.db import models

from accounts.models import User
from company.models import Company


class Review(models.Model):
    RATING_CHOICES = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    )
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    pub_date = models.DateTimeField('date published')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.CharField(max_length=600)
    rating = models.IntegerField(choices=RATING_CHOICES)
    likes = models.ManyToManyField(User, blank=True, related_name='likes')

    class Meta:
        ordering = ['-pub_date']


class Cluster(models.Model):
    name = models.CharField(max_length=100)
    users = models.ManyToManyField(User)

    def get_members(self):
        return "\n".join([u.username for u in self.users.all()])


class ReviewImage(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='photos')
    img = models.ImageField(upload_to='review_company_photos', null=True)
    alt = models.CharField(max_length=256, null=True, default="")

    def __str__(self):
        return self.img.url
