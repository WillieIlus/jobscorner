from django.urls import path

from . import views

app_name = 'reviews'

urlpatterns = [
    path('', views.review_list, name='list'),
    path('<review_id>[0-9]/', views.review_detail, name='review_detail'),
    path('company/<company_id>[0-9]/add_review/', views.add_review, name='new'),
    path('user/<username>/', views.user_review_list, name='user_review_list'),
    path('review/user/', views.user_review_list, name='user_review_list'),


]