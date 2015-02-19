from django.test import TestCase
from rango.models import Category
from rango.helpers import add_cat
from django.core.urlresolvers import reverse

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


