from django.urls import path

from . import views

app_name = 'pricelist'

urlpatterns = [
    path('<slug:slug>/', views.DetailView.as_view(), name='detail'),
    path('<slug:slug>/results/', views.ResultsView.as_view(), name='edit'),

    path('', views.ListView.as_view(), name='list'),
    path('<service_id>/add_price/', views.add_price, name='add_price'),

]
