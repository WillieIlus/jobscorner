from django.forms import ModelForm
from django.test import TestCase
from django.urls import reverse, resolve

from accounts.models import User
from category.forms import CategoryForm
from category.models import Category
from category.views import CategoryCreate, CategoryDetail, CategoryList, CategoryUpdate
from homepage.views import HomeIndex


class HomeTests(TestCase):
    def setUp(self):
        # self.category = Category.objects.create(name='Graphic Design', description='The quick brown')
        url = reverse('home')
        self.response = self.client.get(url)

    def test_home_view_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_home_url_resolves_view(self):
        view = resolve('/')
        self.assertEquals(view.func.view_class, HomeIndex)

    def test_home_view_contains_navigation_links(self):
        home_url = reverse('home')
        category_url = reverse('category:list')
        company_url = reverse('company:list')
        job_url = reverse('job:list')
        location_url = reverse('location:list')
        reviews_url = reverse('reviews:list')
        category_detail_url = reverse('category:detail', kwargs={'slug': 'art'})
        response = self.client.get(home_url)
        self.assertContains(response, home_url)
        self.assertContains(response, category_url)
        self.assertContains(response, company_url)
        self.assertContains(response, job_url)
        self.assertContains(response, location_url)
        self.assertContains(response, reviews_url)
        self.assertContains(response, category_detail_url)



    #
    #
    # def test_detail_url_resolves_view(self):
    #     view = resolve('/category/graphic-design/')
    #     self.assertEquals(view.func.view_class, CategoryDetail)
    #
    # def test_detail_view_contains_navigation_links(self):
    #     detail_url = reverse('category:detail', kwargs={'slug': 'graphic-design'})
    #     list_url = reverse('category:list')
    #     update_url = reverse('category:update', kwargs={'slug': 'graphic-design'})
    #     response = self.client.get(detail_url)
    #     self.assertContains(response, list_url)
    #     self.assertContains(response, update_url)

#
# class NewCategoryTest(TestCase):
#     def setUp(self):
#         Category.objects.create(name='Graphic Design', description='The quick brown fox jumps over the lazy dog')
#         User.objects.create_user(username='john', email='john@doe.com', password='123')
#         self.client.login(username='john', password='123')
#
#     def test_new_category_view_success_status_code(self):
#         url = reverse('category:new')
#         response = self.client.get(url)
#         self.assertEquals(response.status_code, 200)
#
#     def test_new_category_view_not_found_status_code(self):
#         url = reverse('category:new')
#         response = self.client.get(url)
#         self.assertEquals(response.status_code, 404)
#
#     def test_new_category_url_resolves_new_topic_view(self):
#         view = resolve('/category/new/')
#         self.assertEquals(view.func.view_class, CategoryCreate)
#
#     def test_new_category_view_contains_link_back_to_board_topics_view(self):
#         new_category_url = reverse('category:new')
#         home_url = reverse('category:list')
#         response = self.client.get(new_category_url)
#         self.assertContains(response, 'href="{0}"'.format(home_url))
#
#     def test_csrf(self):
#         url = reverse('category:new')
#         response = self.client.get(url)
#         self.assertContains(response, 'csrfmiddlewaretoken')
#
#     def test_contains_form(self):
#         url = reverse('category:new')
#         response = self.client.get(url)
#         form = response.context.get('form')
#         self.assertIsInstance(form, CategoryForm)
#
#     def test_new_category_valid_post_data(self):
#         url = reverse('category:new')
#         data = {
#             'name': 'Test title',
#             'description': 'Lorem ipsum dolor sit amet'
#         }
#         self.client.post(url, data)
#         self.assertTrue(Category.objects.exists())
#
#     def test_new_category_invalid_post_data(self):
#         '''
#         Invalid post data should not redirect
#         The expected behavior is to show the form again with validation errors
#         '''
#         url = reverse('category:new')
#         response = self.client.post(url, {})
#         form = response.context.get('form')
#         self.assertEquals(response.status_code, 200)
#         self.assertTrue(form.errors)
#
#     def test_new_category_invalid_post_data_empty_fields(self):
#         '''
#         Invalid post data should not redirect
#         The expected behavior is to show the form again with validation errors
#         '''
#         url = reverse('category:new')
#         data = {
#             'subject': '',
#             'message': ''
#         }
#         response = self.client.post(url, data)
#         self.assertEquals(response.status_code, 200)
#         self.assertFalse(Category.objects.exists())
#
#
# class LoginRequiredNewCategoryTests(TestCase):
#     def setUp(self):
#         Category.objects.create(name='Graphic Design', description='The quick brown fox jumps over the lazy dog')
#         self.url = reverse('category:new')
#         self.response = self.client.get(self.url)
#
#     def test_redirection(self):
#         login_url = reverse('accounts:login')
#         self.assertRedirects(self.response, '{login_url}?next={url}'.format(login_url=login_url, url=self.url))
#
#
# class CategoryUpdateViewTestCase(TestCase):
#
#     def setUp(self):
#         self.category = Category.objects.create(name='Graphic Design',
#                                                 description='The quick brown fox jumps over the lazy dog')
#         self.url = reverse('category:new')
#         self.username = 'john'
#         self.password = '123'
#         user = User.objects.create_user(username=self.username, email='john@doe.com', password=self.password)
#
#
# class LoginRequiredCategoryUpdateViewTests(CategoryUpdateViewTestCase):
#     def test_redirection(self):
#         '''
#         Test if only logged in users can edit the posts
#         '''
#         login_url = reverse('accounts:login')
#         response = self.client.get(self.url)
#         self.assertRedirects(response, '{login_url}?next={url}'.format(login_url=login_url, url=self.url))
#
#
# class CategoryUpdateViewTests(CategoryUpdateViewTestCase):
#     def setUp(self):
#         super().setUp()
#         self.client.login(username=self.username, password=self.password)
#         self.response = self.client.get(self.url)
#
#     def test_status_code(self):
#         self.assertEquals(self.response.status_code, 200)
#
#     def test_view_class(self):
#         view = resolve('/category/graphic-design/edit/')
#         self.assertEquals(view.func.view_class, CategoryUpdate)
#
#     def test_csrf(self):
#         self.assertContains(self.response, 'csrfmiddlewaretoken')
#
#     def test_contains_form(self):
#         form = self.response.context.get('form')
#         self.assertIsInstance(form, ModelForm)
#
#
# class SuccessfulCategoryUpdateViewTests(CategoryUpdateViewTestCase):
#     def setUp(self):
#         super().setUp()
#         self.client.login(username=self.username, password=self.password)
#         self.response = self.client.post(self.url, {'message': 'edited message'})
#
#     def test_redirection(self):
#         '''
#         A valid form submission should redirect the user
#         '''
#         category_list_url = reverse('category:detail', kwargs={'slug': 'graphic-design'})
#         self.assertRedirects(self.response, category_list_url)
#
#     def test_category_changed(self):
#         self.category.refresh_from_db()
#         self.assertEquals(self.category.description, 'The quick brown fox jumps over the lazy dog')
#
#
# class InvalidCategoryUpdateViewTests(CategoryUpdateViewTestCase):
#     def setUp(self):
#         '''
#         Submit an empty dictionary to the `reply_topic` view
#         '''
#         super().setUp()
#         self.client.login(username=self.username, password=self.password)
#         self.response = self.client.post(self.url, {})
#
#     def test_status_code(self):
#         '''
#         An invalid form submission should return to the same page
#         '''
#         self.assertEquals(self.response.status_code, 200)
#
#     def test_form_errors(self):
#         form = self.response.context.get('form')
#         self.assertTrue(form.errors)
