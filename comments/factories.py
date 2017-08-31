from django.contrib.sites.models import Site
from django.utils import timezone

import factory
from blog.factories import PostFactory
from factory.django import DjangoModelFactory
from users.factories import UserFactory

from .models import BlogComment


class SiteFactory(DjangoModelFactory):
    class Meta:
        model = Site
        django_get_or_create = ('domain',)

    name = 'test'
    domain = 'test.com'


class BlogCommentFactory(DjangoModelFactory):
    class Meta:
        model = BlogComment

    site = factory.SubFactory(SiteFactory)
    content_object = factory.SubFactory(PostFactory)
    user = factory.SubFactory(UserFactory)
    comment = factory.Sequence(lambda n: 'comment %s' % n)
    submit_date = factory.LazyFunction(timezone.now)
