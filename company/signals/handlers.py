from django.conf import settings


def create_notice_types():
    if "pinax.notifications" in settings.INSTALLED_APPS:
        from pinax.notifications.models import NoticeType
        print("Creating notices for company")
        NoticeType.create('new_company', ' New Company ', 'There is a company added')
    else:
        print("Notification app not found")
