from django.urls import path

from .views import LocationCreate, LocationDetail, LocationList, LocationEdit, LocationDelete

app_name = 'location'

urlpatterns = [
    path('new/', LocationCreate.as_view(), name='new'),
    path('<slug:slug>/', LocationDetail.as_view(), name='detail'),
    path('<slug:slug>/edit', LocationEdit.as_view(), name='edit'),
    path('<slug:slug>/delete/', LocationDelete.as_view(), name='delete'),

    path('', LocationList.as_view(), name='list'),

]
