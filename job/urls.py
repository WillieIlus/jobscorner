from django.urls import path

from .views import JobList, JobEdit, JobDelete, JobDetail

app_name = 'job'

urlpatterns = [
    # path('new/', JobCreate.as_view(), name='new'),
    # path('<slug:slug>/edit/', JobEdit.as_view(), name='edit'),
    path('<slug:slug>delete/', JobDelete.as_view(), name='delete'),
    path(r'<slug:slug>/', JobDetail.as_view(), name='detail'),
    path('', JobList.as_view(), name='list'),
]
