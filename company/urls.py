from django.urls import path

from job.views import JobCreate, JobEdit
from .views import CompanyCreate, CompanyDetail, CompanyList, CompanyEdit, CompanyDelete

app_name = 'company'

urlpatterns = [
    path('new/', CompanyCreate.as_view(), name='new'),
    path('<slug:slug>/', CompanyDetail.as_view(), name='detail'),
    path('<slug:slug>/edit/', CompanyEdit.as_view(), name='edit'),
    path('<slug:slug>/delete/', CompanyDelete.as_view(), name='delete'),
    path('<slug:slug>/new/', JobCreate.as_view(), name='new_job'),
    path('<slug:slug>/job/edit/', JobEdit.as_view(), name='edit_job'),

    path('', CompanyList.as_view(), name='list'),

]
