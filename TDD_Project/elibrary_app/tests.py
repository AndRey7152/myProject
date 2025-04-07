from django.test import TestCase, SimpleTestCase
from django.urls import reverse
from django.urls.base import resolve

from .views import home
from .models import Catalog
from .forms import AddBookForm
# Create your tests here.

class CatalogModelTests(TestCase):
    '''Тест модели каталога'''
    def setUp(self):
        self.book = Catalog(
            title = 'First Django Book',
            ISBN = '978-1-60309-3',
            author = 'Ilya Perminov',
            price = '9.99',
            availability = 'True'
        )

    def test_create_book(self):
        self.assertIsInstance(self.book, Catalog)

    def test_str_representation(self):
        self.assertEqual(str(self.book), 'First Django Book')

    def test_saving_and_retrieving_book(self):
        first_book = Catalog()
        first_book.title = 'First Django Book'
        first_book.ISBN = '978-1-60309-3'
        first_book.author  = 'Ilya Perminov'
        first_book.price = '9.99'
        first_book.availability = 'True'
        first_book.save()

        second_book = Catalog()
        second_book.title = 'Second Django Book'
        second_book.ISBN = '989-3-60124-1'
        second_book.author = 'Dmitry Seleznev'
        second_book.price = '19.99'
        second_book.availability = 'False'
        second_book.save()

        saved_books = Catalog.objects.all()
        self.assertEqual(saved_books.count(), 2)

        first_saved_book = saved_books[0]
        second_saved_book = saved_books[1]
        self.assertEqual(first_saved_book.title, 'First Django Book')
        self.assertEqual(second_saved_book.author, 'Dmitry Seleznev')


class ElibraryURLsTest(TestCase):
    ''' Тестируем Urls '''

    def test_homepage_url_name(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_root_url_resolves_to_homepage_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home)

class CatalogFormTests(TestCase):
    ''' Тесты для форм '''
    def setUp(self):
        url = reverse('home')
        self.response = self.client.get(url)

    def test_book_form(self):
        form = self.response.context.get('add_book_form')
        self.assertIsInstance(form, AddBookForm)
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_bootstrap_class_used_for_default_styling(self):
        form = self.response.context.get('add_book_form')
        self.assertIn('class="form-control"', form.as_p())

    def test_book_form_validation_for_blank_items(self):
        add_book_form = AddBookForm(
            data={'title': '', 'ISBN': '', 'author': '', 'price': '', 'availability': ''}
        )
        self.assertFalse(add_book_form.is_valid())

class CatalogTemplateTests(TestCase):
    ''' Тест шаблона '''

    def setUp(self):
        url = reverse('home')
        self.response = self.client.get(url)

    def test_homepage_template(self):
        self.assertTemplateUsed(self.response, 'home.html')

    def test_homepage_contains_correct_html(self):
        self.assertContains(self.response, 'E-library Application')

    def test_homepage_does_not_contain_incorrect_html(self):
        self.assertNotContains(self.response, 'Hello World')

class CatalogViewTests(TestCase):
    ''' Тест для представления  '''
    def test_book_list_view(self):

        Book_1 = Catalog.objects.create(
            title = 'Django for Beginners (2018)',
            ISBN = '978-1-60309-0',
            author = 'John Doe',
            price = '9.99',
            availability = True
        )

        Book_2 = Catalog.objects.create(
            title = 'Django for Professionals (2020)',
            ISBN = '978-1-60309-3',
            author = 'Mary Doe',
            price = '11.99',
            availability = False
        )

        response = self.client.get(reverse('home'))

        self.assertIn('Django for Professionals (2020)', response.content.decode())
        self.assertIn('John Doe', response.content.decode())
        self.assertIn('978-1-60309-3', response.content.decode())