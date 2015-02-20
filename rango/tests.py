from django.test import TestCase
from rango.models import Category, Page
from rango.helpers import add_cat
from django.core.urlresolvers import reverse
from datetime import datetime, timedelta

# Create your tests here.
class CategoryMethodTest(TestCase):

    def test_ensure_views_are_positive(self):
        cat = Category(name='test', view=-1, likes=0)
        cat.save()
        self.assertEqual((cat.view >= 0), True)

    def test_slug_line_creation(self):
        cat = Category(name='Random Category String')
        cat.save()
        self.assertEqual(cat.slug, 'random-category-string')

class IndexViewTest(TestCase):

    def test_index_view_with_no_categories(self):
        response = self.client.get(reverse('index'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "There are no categories present.")
        self.assertQuerysetEqual(response.context['categories'], [])

    def test_index_view_with_categories(self):
        add_cat('test',1,1)
        add_cat('temp',1,1)
        add_cat('tmp',1,1)
        add_cat('tmp test temp',1,1)

        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'tmp test temp')
        num_cats = len(response.context['categories'])
        self.assertEqual(num_cats, 4)

class PageMethodTest(TestCase):

    def test_first_view_is_not_in_future(self):
        cat = add_cat('test', 1, 1)
        page = Page(category=cat, title='testpage', url='http://example.com',
         views=0, first_visit= datetime.now() + timedelta(days=30), last_visit=datetime.now())
        page.save()
        self.assertEqual((page.first_visit <= datetime.now()), True)

    def test_last_view_is_not_in_future(self):
        cat = add_cat('test', 1, 1)
        page = Page(category=cat, title='testpage', url='http://example.com',
         views=0, first_visit= datetime.now(), last_visit=datetime.now() + timedelta(days=30))
        page.save()
        self.assertEqual((page.last_visit <= datetime.now()), True)

    def test_last_visit_equal_to_or_after_the_first_visit(self):
        cat = add_cat('test', 1, 1)
        page = Page(category=cat, title='testpage', url='http://example.com',
         views=0, first_visit= datetime.now() + timedelta(days=30),
         last_visit=datetime.now() - timedelta(days=30))
        page.save()
        self.assertEqual((page.last_visit >= page.first_visit), True)