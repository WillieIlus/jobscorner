from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST
from django.views.generic import DetailView, ListView, UpdateView, CreateView, DeleteView

# Job views
from accounts.decorators import UserRequiredMixin
from company.models import Company
from job.forms import JobForm
from job.models import Job


class JobCreate(LoginRequiredMixin, CreateView):
    model = Job
    form_class = JobForm
    template_name = 'form.html'

    def form_valid(self, form):
        form.instance.company = get_object_or_404(Company, slug=self.kwargs['slug'])
        form.instance.user = self.request.user
        form.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        """
        If the form is invalid, re-render the context data with the
        data-filled form and errors.
        """
        print('the is an error in your form' )
        messages.warning(self.request, 'There was an error in this form')
        return self.render_to_response(self.get_context_data(form=form))

    def get_success_url(self):
        return reverse_lazy('job:list')


class JobEdit(LoginRequiredMixin, UserRequiredMixin, UpdateView):
    model = Job
    form_class = JobForm
    template_name = 'form.html'

    # def get_form(self, *args, **kwargs):
    #     form = super().get_form(*args, **kwargs)
    #     form.fields['company'].queryset = Company.objects.filter(user=self.request.user)
    #     return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = " Update Job "
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def form_invalid(self, form):
        """
        If the form is invalid, re-render the context data with the
        data-filled form and errors.
        """
        messages.warning(self.request, '{0} error')
        return self.render_to_response(self.get_context_data(form=form))


class JobList(ListView):
    model = Job
    context_object_name = 'job'
    template_name = 'job/list.html'


class JobDetail(DetailView):
    model = Job
    context_object_name = 'job'
    template_name = 'job/detail.html'


class JobDelete(LoginRequiredMixin, UserRequiredMixin, DeleteView):
    model = Job
    success_url = reverse_lazy('job_list')
    template_name = 'delete.html'


@login_required
@require_POST
def job_like(request):
    job_id = request.POST.get('slug')
    action = request.POST.get('action')
    if job_id and action:
        try:
            job = Job.objects.get(id=job_id)
            if action == 'like':
                job.users_like.add(request.user)
            else:
                job.users_like.remove(request.user)
            return JsonResponse({'status':'ok'})
        except:
            pass
    return JsonResponse({'status':'ko'})