from django import template

from job.models import Job

register = template.Library()


@register.simple_tag
def total_jobs():
    return Job.objects.count()


@register.inclusion_tag('job/latest_jobs.html')
def show_latest_jobs(count=5):
    latest_jobs = Job.objects.order_by('-publish')[:count]
    return {'latest_jobs': latest_jobs}


@register.inclusion_tag('job/latest_of_jobs.html')
def show_latest_of_jobs(count=5):
    latest_jobs = Job.objects.order_by('-publish')[:count]
    return {'latest_jobs': latest_jobs}
