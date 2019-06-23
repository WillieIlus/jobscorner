from django import template

from pricelist.models import Service

register = template.Library()


@register.simple_tag
def total_services():
    return Service.objects.count()


@register.inclusion_tag('prices/services.html')
def show_services(count=10):
    services = Service.objects.order_by('name')[:count]
    return {'services': services}


@register.inclusion_tag('prices/random-services.html')
def random_services(count=6):
    services = Service.objects.order_by('name')[:count]
    return {'services': services}
