from django.urls import path

from .views import JobList, JobEdit, JobDelete, JobDetail, job_like

app_name = 'job'

urlpatterns = [
    # path('new/', JobCreate.as_view(), name='new'),
    # path('<slug:slug>/edit/', JobEdit.as_view(), name='edit'),
    path('<slug:slug>delete/', JobDelete.as_view(), name='delete'),
    path('<slug:slug>/', JobDetail.as_view(), name='detail'),
    path('', JobList.as_view(), name='list'),
    path('like/', job_like, name='like'),
]
