from django.forms import ModelForm
from django.test import TestCase
from django.urls import reverse, resolve

from accounts.models import User
from country.models import Country
from country.views import CountryList, CountryDetail, CountryEdit


class CountryListTests(TestCase):
    def setUp(self):
        self.country = Country.objects.create(name='Kenya',
                               description='Kenya is a sorveign county, it is capital is nairobi',
                               website='www.kenya.com')
        url = reverse('country:list')
        self.response = self.client.get(url)

    def test_list_view_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_list_url_resolves_view(self):
        view = resolve('/country/')
        self.assertEquals(view.func.view_class, CountryList)

    def test_list_view_contains_navigation_links(self):
        country_detail_url = reverse('country:detail', kwargs={'slug': 'kenya'})
        response = self.client.get(country_detail_url)
        self.assertContains(response, country_detail_url)


class CountryDetailTests(TestCase):
    def setUp(self):
        self.country = Country.objects.create(name='Kenya',
                               description='Kenya is a sovereign county, it is capital is Nairobi',
                               website='www.kenya.com')

    def test_detail_view_success_status_code(self):
        url = reverse('country:detail', kwargs={'slug': 'kenya'})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_detail_view_not_found_status_code(self):
        url = reverse('country:detail', kwargs={'slug': 'nothing-to-show-here'})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)

    def test_detail_url_resolves_view(self):
        view = resolve('/country/kenya/')
        self.assertEquals(view.func.view_class, CountryDetail)

    def test_detail_view_contains_navigation_links(self):
        detail_url = reverse('country:detail', kwargs={'slug': 'kenya'})
        list_url = reverse('country:list')
        edit_url = reverse('country:edit', kwargs={'slug': 'kenya'})
        response = self.client.get(detail_url)
        self.assertContains(response, list_url)
        self.assertContains(response, edit_url)


class CountryUpdateViewTestCase(TestCase):
    def setUp(self):
        self.country = Country.objects.create(name='Kenya',
                                              description='The quick brown fox jumps over the lazy dog',
                                              website='www.kenya.com')
        self.url = reverse('country:edit', kwargs={'slug': 'kenya'})
        self.username = 'john'
        self.password = '123'
        user = User.objects.create_user(username=self.username, email='john@doe.com', password=self.password)


class LoginRequiredCountryUpdateViewTests(CountryUpdateViewTestCase):
    def test_redirection(self):
        '''
        Test if only logged in users can edit the posts
        '''
        login_url = reverse('accounts:login')
        response = self.client.get(self.url)
        self.assertRedirects(response, '{login_url}?next={url}'.format(login_url=login_url, url=self.url))


class CountryUpdateViewTests(CountryUpdateViewTestCase):
    def setUp(self):
        super().setUp()
        self.client.login(username=self.username, password=self.password)
        self.response = self.client.get(self.url)

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_view_class(self):
        view = resolve('/country/kenya/edit/')
        self.assertEquals(view.func.view_class, CountryEdit)

    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_contains_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, ModelForm)


class SuccessfulCountryUpdateViewTests(CountryUpdateViewTestCase):
    def setUp(self):
        super().setUp()
        self.client.login(username=self.username, password=self.password)
        self.response = self.client.post(self.url)

    def test_redirection(self):
        '''
        A valid form submission should redirect the user
        '''
        country_list_url = reverse('country:detail', kwargs={'slug': 'kenya'})
        self.assertRedirects(self.response, country_list_url)

    def test_country_changed(self):
        self.country.refresh_from_db()
        self.assertEquals(self.country.description, 'The quick brown fox jumps over the lazy dog')


class InvalidCategoryUpdateViewTests(CountryUpdateViewTestCase):
    def setUp(self):
        '''
        Submit an empty dictionary to the `reply_topic` view
        '''
        super().setUp()
        self.client.login(username=self.username, password=self.password)
        self.response = self.client.post(self.url, {})

    def test_status_code(self):
        '''
        An invalid form submission should return to the same page
        '''
        self.assertEquals(self.response.status_code, 200)

    def test_form_errors(self):
        form = self.response.context.get('form')
        self.assertTrue(form.errors)
