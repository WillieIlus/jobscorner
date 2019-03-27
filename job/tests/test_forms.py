from django.test import Client, TestCase
from django.urls import reverse

from accounts.models import User
from category.models import Category
from company.models import Company
from country.models import Country
from job.forms import JobForm
from job.models import Job
from location.models import Location


class TestForms(TestCase):
    def setUp(self):
        self.client = Client()
        self.list_url = reverse('job:list')
        self.detail_url = reverse('job:detail', kwargs={'slug': 'job-vacancy'})
        self.detail_url_404 = reverse('job:detail', kwargs={'slug': 'nothing_to_show'})
        self.edit_url = reverse('job:edit', kwargs={'slug': 'job-vacancy'})
        self.login_url = reverse('accounts:login')

        self.user = User.objects.create_user(
            username='123',
            email='john@doe.com',
            password='john'
        )
        self.country = Country.objects.create(
            name='Kenya',
            description='Kenya is a sorveign country, it is capital is nairobi',
            website='www.kenya.com'
        )
        self.location = Location.objects.create(
            name='Nairobi',
            country=self.country,
            description='the quick'
        )
        self.category = Category.objects.create(
            name='Graphic Design',
            description='The quick brown'
        )
        self.company = Company.objects.create(
            name='brandlogic',
            description='lorem ipsum',
            user=self.user,
            category=self.category,
            website='www.brandlogic.com',
            email='brand@logic.com'
        )
        Job.objects.create(
            user=self.user,
            title='Job Vacancy',
            salary='1000',
            description='job vacant in nairobi',
            work_hours='8 hours',
            contact_email='contact@email.com',
            location=self.location,
            category=self.category,
            company=self.company,
            remote='True',
        )

    def test_job_form_valid_data(self):
        form = JobForm(data={
            'title': 'Job Vacant',
            'salary': '3000',
            'description': 'The Quick',
            'qualification': 'Brown Fox',
            'responsibilities': 'Jumped Over',
            'requirements': 'the lazy',
            'benefits': 'dog',
            'application': 'the quick',
            'work_hours': '8 hours',
            'url': 'www.quick.com',
            'contact_email': 'quick@brown.com',
            'experience': '12 years',
            'location': 'self.location',
            'category': 'self.category',
            'remore': 'True',
            'company': 'self.company',
        })

        self.assertTrue(form.is_valid())

    def test_job_form_no_data(self):
        form = JobForm(data={})

        self.assertFalse(form.is_valid())

    # def test_job_update_view_login_redirection(self):
    #     response = self.client.get(self.edit_url)
    #     self.assertRedirects(response, '{login_url}?next={url}'.format(login_url=self.login_url, url=self.edit_url))
    #
    # def test_job_update_view_status_code(self):
    #     self.response = self.client.get(self.edit_url)
    #     self.assertEquals(self.response.status_code, 200)

    # def test_job_update_view_class(self):
    #     view = resolve('/job/job-vacancy/edit/')
    #     self.assertEquals(view.func.view_class, JobEdit)
    #
    # def test_job_update_view_csrf(self):
    #     self.response = self.client.get(self.edit_url)
    #
    #     self.assertContains(self.response, 'csrfmiddlewaretoken')
    #
    # def test_job_update_view_contains_form(self):
    #     self.response = self.client.get(self.edit_url)
    #
    #     form = self.response.context.get('form')
    #     self.assertIsInstance(form, ModelForm)
    #
    # def test_job_update_view_success_redirection(self):
    #     list_url = reverse('job:detail', kwargs={'slug': 'job-vacancy'})
    #     self.assertRedirects(self.response, list_url)
    # self.assertRedirects(self.response, self.list_url)
    #
    # def test_job_update_view_changed(self):
    #     Job.refresh_from_db(self)
    #     self.assertEquals(Job.description, 'The quick brown fox jumps over the lazy dog')
    #
    # def test_job_update_view_invalid_status_code(self):
    #     self.assertEquals(self.response.status_code, 200)
    #
    # def test_job_update_view_invalid_form_errors(self):
    #     form = self.response.context.get('form')
    #     self.assertTrue(form.errors)
