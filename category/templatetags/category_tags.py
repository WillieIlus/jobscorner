from django import template

from category.models import Category

register = template.Library()


@register.simple_tag
def total_categories():
    return Category.objects.count()


@register.inclusion_tag('category/categories.html')
def show_categories(count=6):
    categories = Category.objects.order_by('name')[:count]
    return {'categories': categories}


@register.inclusion_tag('category/random-categories.html')
def random_categories(count=6):
    categories = Category.objects.order_by('name')[:count]
    return {'categories': categories}
