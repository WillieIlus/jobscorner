from django.urls import path

from .views import CountryEdit, CountryDetail, CountryList

app_name = 'country'

urlpatterns = [
    path('<slug:slug>/', CountryDetail.as_view(), name='detail'),
    path('<slug:slug>/edit/', CountryEdit.as_view(), name='edit'),
    path('', CountryList.as_view(), name='list'),

]
