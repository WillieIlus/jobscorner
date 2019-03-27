from django.forms import ModelForm
from django.test import TestCase
from django.urls import reverse, resolve

from accounts.models import User
from country.models import Country
from location.models import Location
from location.views import LocationCreate, LocationList, LocationEdit


class LocationListTests(TestCase):
    def setUp(self):
        country = Country.objects.create(name='Kenya',
                                         description='Kenya is a sovereign county, it is capital is Nairobi',
                                         website='www.kenya.com')

        Location.objects.create(name='Nairobi', country=country,
                                                description='the quick')
        url = reverse('location:list')
        self.response = self.client.get(url)

    def test_list_view_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_list_url_resolves_view(self):
        view = resolve('/location/')
        self.assertEquals(view.func.view_class, LocationList)

    def test_list_view_contains_detail_links(self):
        location_detail_url = reverse('location:detail', kwargs={'slug': 'nairobi'})
        response = self.client.get(location_detail_url)
        self.assertContains(response, location_detail_url)

    def test_list_view_contains_new_links(self):
        location_add_url = reverse('location:add')
        response = self.client.get(location_add_url)
        self.assertContains(response, location_add_url)


class LocationDetailTests(TestCase):
    def setUp(self):

        country = Country.objects.create(name='Kenya',
                                         description='Kenya is a sovereign county, it is capital is Nairobi',
                                         website='www.kenya.com')

        Location.objects.create(name='Nairobi', country=country,
                                                description='the quick')
        User.objects.create_user(username='john', email='john@gmail.com', password='1234john')
        self.client.login(username='john', password='1234john')

    def test_location_view_success_status_code(self):
        url = reverse('location:detail', kwargs={'slug': 'nairobi'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_location_view_not_found_status_code(self):
        url = reverse('location:detail', kwargs={'slug': 'kenya'})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)

    def test_location_url_resolves_location_view(self):
        view = resolve('/location/add/')
        self.assertEquals(view.func.view_class, LocationCreate)

    def test_location_view_contains_link_back_to_location_list_view(self):
        location_url = reverse('location:detail', kwargs={'slug': 'nairobi'})
        location_list_url = reverse('location:list')
        response = self.client.get(location_url)
        self.assertContains(response, location_list_url)


class LocationUpdateViewTestCase(TestCase):
    def setUp(self):
        country = Country.objects.create(name='Kenya',
                                         description='Kenya is a sovereign county, it is capital is Nairobi',
                                         website='www.kenya.com')
        Location.objects.create(name='Nairobi', country=country,
                                                description='the quick.')
        self.url = reverse('location:update', kwargs={'slug': 'nairobi'})
        self.username = 'john'
        self.password = '1234john'
        self.user = User.objects.create_user(username=self.username, email='john@gmail.com', password=self.password)


class LoginRequiredLocationUpdateViewTests(LocationUpdateViewTestCase):
    def test_redirection(self):
        '''
        Test if only logged in users can edit the posts
        '''
        login_url = reverse('accounts:login')
        response = self.client.get(self.url)
        self.assertRedirects(response, '{login_url}?next={url}'.format(login_url=login_url, url=self.url))


class LocationUpdateViewTests(LocationUpdateViewTestCase):
    def setUp(self):
        super().setUp()
        self.client.login(username=self.username, password=self.password)
        self.response = self.client.get(self.url)

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_view_class(self):
        view = resolve('/location/kenya/edit/')
        self.assertEquals(view.func.view_class, LocationEdit)

    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_contains_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, ModelForm)


class SuccessfulLocationUpdateViewTests(LocationUpdateViewTestCase):
    def setUp(self):
        super().setUp()
        self.client.login(username=self.username, password=self.password)
        self.response = self.client.post(self.url, {'message': 'edited message'})

    def test_redirection(self):
        '''
        A valid form submission should redirect the user
        '''
        location_list_url = reverse('location:detail', kwargs={'slug': 'nairobi'})
        self.assertRedirects(self.response, location_list_url)

    def test_location_changed(self):
        self.location.refresh_from_db()
        self.assertEquals(self.location.description, 'The quick brown fox jumps over the lazy dog')


class InvalidCategoryUpdateViewTests(LocationUpdateViewTestCase):
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
