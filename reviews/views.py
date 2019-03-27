import datetime

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views.generic import CreateView

from company.models import Company
from .forms import ReviewForm
from .models import Review


# from .suggestions import update_clusters


def review_list(request):
    latest_review_list = Review.objects.order_by('-pub_date')[:9]
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


def user_review_list(request, username=None):
    if not username:
        username = request.user.username
    latest_review_list = Review.objects.filter(user=username).order_by('-pub_date')
    context = {'latest_review_list': latest_review_list, 'username': username}
    return render(request, 'reviews/user_review_list.html', context)


#
# @login_required
# def like_review(request, company_id, review_id):
#     company = get_object_or_404(Review, pk=company_id, id=review_id)
#     review = get_object_or_404(Review, pk=request.POST.get('company_id'), id=request.POST.get('review_id'))
#     review.likes.add(request.user)
#     return HttpResponseRedirect(reverse('company:detail', args=(company.slug,)))


class LikeReviewView(LoginRequiredMixin, CreateView):
    # template_name = 'qa/create_comment.html'
    model = Review
    # fields = ['comment_text']
    message = 'Thank you! your comment has been posted.'

    def post(self, request, review_id):
        # vote_target = get_object_or_404(self.model, pk=object_id)
        review = get_object_or_404(Review, pk=request.POST.get('review_id'))
        review.likes.add(request.user)
        return HttpResponseRedirect(reverse('company:detail', args=(company.slug,)))
