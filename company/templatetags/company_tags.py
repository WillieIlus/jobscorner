from company.models import Company
from django import template

register = template.Library()


@register.simple_tag
def total_companies():
    return Company.objects.count()


@register.inclusion_tag('company/latest_companies.html')
def show_latest_companies(count=5):
    latest_companies = Company.objects.order_by('-publish')[:count]
    return {'latest_companies': latest_companies}
