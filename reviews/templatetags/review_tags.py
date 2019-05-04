from django import template

from reviews.models import Review

register = template.Library()


@register.simple_tag
def total_reviews():
    return Review.objects.count()


@register.inclusion_tag('reviews/latest_reviews.html')
def show_latest_reviews(count=5):
    latest_reviews = Review.objects.order_by('-publish')[:count]
    return {'latest_reviews': latest_reviews}

