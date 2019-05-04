import datetime

from company.models import Company
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, request
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views.generic import ListView, DetailView

from .forms import ReviewForm
from .models import Review


# from .suggestions import update_clusters

class ReviewList(ListView):

    queryset = Review.objects.order_by('-publish')[:9]
    context_object_name = 'review'
    template_name = 'reviews/list.html'


class ReviewDetail(DetailView):
    model = Review
    context_object_name = 'review'
    template_name = 'reviews/detail.html'


def user_review_list(request, username=None):
    if not username:
        username = request.user.username
    latest_review_list = Review.objects.filter(user_name=username).order_by('-publish')
    context = {'latest_review_list':latest_review_list, 'username':username}
    return render(request, 'reviews/user_review_list.html', context)


class UserReviews(ListView):
    context_object_name = 'review'
    template_name = 'reviews/user_reviews.html'

    def get_queryset(self):
        user = self.request.user
        return Review.objects.filter(user=user).order_by('-publish')
        # Question.objects.order_by('-pub_date')[:5]


def review_list(request):
    latest_review_list = Review.objects.order_by('-publish')[:9]
    context = {'latest_review_list': latest_review_list}
    return render(request, 'reviews/list.html', context)


def review_detail(request, review_id):
    review = get_object_or_404(Review, pk=review_id)
    return render(request, 'reviews/detail.html', {'review': review})


@login_required
def add_review(request, company_id):
    company = get_object_or_404(Company, pk=company_id)
    form = ReviewForm(request.POST)
    if form.is_valid():
        rating = form.cleaned_data['rating']
        comment = form.cleaned_data['comment']
        user = request.user.username
        review = Review()
        review.company = company
        review.user = request.user
        review.rating = rating
        review.comment = comment
        review.pub_date = datetime.datetime.now()
        review.save()
        '''
        Always return an HttpResponseRedirect after successfully dealing
        with POST data. This prevents data from being posted twice if a
        user hits the Back button.
        '''
        return HttpResponseRedirect(reverse('company:detail', args=(company.slug,)))
    return render(request, 'company/detail.html', {'company': company, 'form': form})
