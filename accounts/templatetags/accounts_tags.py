from accounts.models import User
from django import template

from resume.models import Profile

register = template.Library()


@register.simple_tag
def total_user():
    return User.objects.count()


@register.inclusion_tag('resume/latest_profile.html')
def show_latest_profile(count=5):
    latest_profile = Profile.objects.order_by('-publish')[:count]
    return {'latest_profile': latest_profile}
