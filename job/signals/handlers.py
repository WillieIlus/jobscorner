from django.conf import settings


def create_notice_types():
    if "pinax.notifications" in settings.INSTALLED_APPS:
        from pinax.notifications.models import NoticeType
        print("Creating notices for job")
        NoticeType.create('new_job', ' Job Vacancy ', 'New Job vacancy created')
    else:
        print("Notification app not found")
