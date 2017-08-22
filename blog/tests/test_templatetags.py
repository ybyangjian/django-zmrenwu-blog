from django.template import Template, Context
import factory

from test_plus import TestCase

from ..templatetags.blog_tags import get_recent_posts, get_categories, archives
from ..factories import PostFactory, CategoryFactory
from ..models import Category, Post


class TemplatetagsTestCase(TestCase):
    def test_get_recent_posts(self):
        pass

    def test_archives(self):
        PostFactory.create_batch(10)
        # self.assertQuerysetEqual(archives(), Post.objects.dates('created_time', 'month', order='DESC'))

    def test_get_categories(self):
        pass

    def test_describe(self):
        pass
