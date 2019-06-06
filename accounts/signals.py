from urllib import request

import actstream
from actstream import action
from django.db.models.signals import post_save
# from django.http import request

from accounts.models import User
from company.models import Company
from job.models import Job
from reviews.models import Review


def my_handler(sender, instance, created, **kwargs):
    action.send(instance, verb='was saved')


post_save.connect(my_handler, sender=User)


# company = Company.objects.get(name='Company')

# # from actstream import action
# # from myapp.models import Group, Comment
# # User, Group & Comment have been registered with
# actstream.registry.register
# # action.send(request.user, verb='Joined Website')
# # ...
# job = Job.objects.get(name='Job')
# group = Group.objects.get(name='MyGroup')
# # action.send(request.user, verb='joined', target=job)
# # ...
# # company = Company.objects.get(name='Company')
# review = Review.create(text=comment_text)
# # action.send(request.user, verb='reviewed', action_object=review, target=job)