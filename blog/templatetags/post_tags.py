from django import template

from blog.models import Post

register = template.Library()


@register.simple_tag
def total_posts():
    return Post.published.count()


@register.inclusion_tag('blog/latest-posts.html')
def latest_posts(count=6):
    latest_posts = Post.published.order_by('-publish')[:count]
    return {'latest_posts': latest_posts}
