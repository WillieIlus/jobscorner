from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic

from company.models import Company
from pricelist.forms import PriceForm
from .models import Service, Price


class ListView(generic.ListView):
    # queryset = Service.objects.published
    model = Service
    template_name = 'prices/list.html'
    context_object_name = 'service_list'


class DetailView(LoginRequiredMixin, generic.DetailView):
    model = Service
    template_name = 'prices/detail.html'
    context_object_name = 'service'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = PriceForm()
        form.fields['company'].queryset = Company.objects.filter(user=self.request.user)
        context['form'] = form

        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)


class ResultsView(generic.DetailView):
    model = Service
    template_name = 'prices/results.html'


@login_required
def add_price(request, service_id):
    service = get_object_or_404(Service, pk=service_id)
    form = PriceForm(request.POST)
    if form.is_valid():
        amount = form.cleaned_data['amount']
        description = form.cleaned_data['description']
        company = form.cleaned_data['company']
        price = Price()
        price.service = service
        price.amount = amount
        price.user = request.user
        price.description = description
        price.company = company
        price.save()
        '''
       Always return an HttpResponseRedirect after successfully dealing
      with POST data. This prevents data from being posted twice if a
      user hits the Back button.
      '''
        return HttpResponseRedirect(reverse('pricelist:detail', args=(service.slug,)))
    return render(request, 'pricelist/detail.html', {'service': service, 'form': form})
