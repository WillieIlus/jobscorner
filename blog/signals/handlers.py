from django.conf import settings


def create_notice_types():
    if "pinax.notifications" in settings.INSTALLED_APPS:
        from pinax.notifications.models import NoticeType
        print("Creating notices for blog")
        NoticeType.create('new_blog', ' Recent Blog Post ', 'Check out this post ')
        NoticeType.create('new_comment', ' Comment ', 'There is a comment added')
    else:
        print("Notification app not found")
