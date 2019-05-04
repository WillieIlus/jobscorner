from django.urls import path

from .views import ProfileCreateView, ProfileList, ProfileDelete, ProfileDetail, EducationCreate, ExperienceCreate, \
    CVPdfDetailView, SkillsCreate

app_name = 'resume'

urlpatterns = [
    path('new/', ProfileCreateView.as_view(), name='new'),
    path('<slug>/', ProfileDetail.as_view(), name='detail'),
    path('<slug>/delete/', ProfileDelete.as_view(), name='delete'),
    path('<slug>/education/new/', EducationCreate.as_view(), name='new_education', ),
    path('<slug>/experience/new/', ExperienceCreate.as_view(), name='new_experience', ),
    path('<slug>/skills/new/', SkillsCreate.as_view(), name='new_skills'),
    path('<slug>/pdf/', CVPdfDetailView.as_view(), name='pdf'),
    path('', ProfileList.as_view(), name='list'),

]
