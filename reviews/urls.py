from django.urls import path

from .views import ReviewList, ReviewDetail, UserReviews, add_review

app_name = 'reviews'

urlpatterns = [
    path('', ReviewList.as_view(), name='list'),
    path('<int:pk>/', ReviewDetail.as_view(), name='detail'),
    path('<int:pk>/user/', UserReviews.as_view(), name='user_reviews'),
    path('<int:pk>/username/', UserReviews.as_view(), name='user_reviews'),
    # path('', views.review_list, name='list'),
    # path('<review_id>[0-9]/', views.review_detail, name='review_detail'),
    path('company/<company_id>[0-9]/add_review/', add_review, name='new'),
    # path('user/<username>/', views.user_review_list, name='user_review_list'),
    # path('review/user/', views.user_review_list, name='user_review_list'),

]
