"""jobcorner URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.contrib.flatpages.views import flatpage
from django.urls import path, include
from django_filters.views import FilterView

from homepage.views import HomeIndex, UserFilter, Dashboard

urlpatterns = [
    path('dashboard', Dashboard.as_view(), name='dashboard'),
    path('', HomeIndex.as_view(), name='home'),
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('company/', include('company.urls', namespace='company')),
    path('category/', include('category.urls', namespace='category')),
    path('country/', include('country.urls', namespace='country')),
    path('location/', include('location.urls', namespace='location')),
    path('job/', include('job.urls', namespace='job')),
    path('resume/', include('resume.urls', namespace='resume')),
    path('reviews/', include('reviews.urls', namespace='reviews')),
    path('blog/', include('blog.urls', namespace='blog')),
    path('search/', FilterView.as_view(filterset_class=UserFilter, template_name='search.html'), name='search'),
    path('reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='accounts/password_reset_done.html'),
         name='password_reset_done'),
    path('reset/', auth_views.PasswordResetView.as_view(template_name='accounts/password_reset.html',
                                                        email_template_name='accounts/password_reset_email.html',
                                                        subject_template_name='accounts/password_reset_subject.txt'),
         name='password_reset'),
    path("likes/", include("pinax.likes.urls", namespace="pinax_likes")),
    path('notifications/', include("pinax.notifications.urls", namespace="notifications")),
    path('messages/', include("pinax.messages.urls", namespace="pinax_messages")),

    path('about-us/', flatpage, {'url': '/about-us/'}, name='about'),
    path('license/', flatpage, {'url': '/license/'}, name='license'),
    path('terms/', flatpage, {'url': '/terms/'}, name='terms'),
    path('pricelist/', include('pricelist.urls', namespace='pricelist')),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
