from django.urls import path

from .views import PostCreate, PostDetail, PostEdit, PostDelete, PostList, add_comment

app_name = 'Post'

urlpatterns = [
    path('new/', PostCreate.as_view(), name='new'),
    path('<slug:slug>/', PostDetail.as_view(), name='detail'),
    path('<slug:slug>/edit/', PostEdit.as_view(), name='edit'),
    path('<slug:slug>/delete/', PostDelete.as_view(), name='delete'),

    path('', PostList.as_view(), name='list'),
    path('<post_id>/add_comment/', add_comment, name='add_comment'),

]


