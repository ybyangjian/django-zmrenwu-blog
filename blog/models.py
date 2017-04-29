from django.db import models
from django.db.models import Sum, Max
from django.conf import settings
from django.utils.six import python_2_unicode_compatible
from django.urls import reverse

import os


@python_2_unicode_compatible
class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Category(models.Model):
    GENRE_CHOICES = (
        (1, 'collection'),
        (2, 'tutorial'),
    )

    STATUS_CHOICES = (
        (1, 'ongoing'),
        (2, 'finished'),
    )

    name = models.CharField(max_length=100)
    title = models.CharField(max_length=255, blank=True)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    created = models.DateTimeField(auto_now=True)
    genre = models.PositiveSmallIntegerField(choices=GENRE_CHOICES)
    status = models.PositiveSmallIntegerField(choices=STATUS_CHOICES, blank=True, null=True)
    cover = models.ImageField(upload_to='covers/categories/%Y/%m/%d/', blank=True)
    resource = models.URLField(blank=True)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('blog:category_slug', kwargs={'slug': self.slug})

    def total_views(self):
        return self.post_set.aggregate(category_views=Sum('views'))

    def last_modified(self):
        return self.post_set.aggregate(last_modified=Max('modified_time'))


def post_cover_path(instance, filename):
    return os.path.join('posts', instance.pk, filename)


@python_2_unicode_compatible
class Post(models.Model):
    STATUS_CHOICES = (
        (1, 'published'),
        (2, 'draft'),
        (3, 'hidden'),
    )

    status = models.PositiveSmallIntegerField(choices=STATUS_CHOICES, blank=True, null=True)
    title = models.CharField(max_length=255)
    body = models.TextField()
    excerpt = models.CharField(max_length=200, blank=True)
    views = models.PositiveIntegerField(default=0, editable=False)
    pub_date = models.DateTimeField(blank=True, null=True)
    created_time = models.DateTimeField()
    modified_time = models.DateTimeField()
    cover = models.ImageField(upload_to=post_cover_path, blank=True)
    category = models.ForeignKey(Category, null=True, blank=True)
    tags = models.ManyToManyField(Tag, blank=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL)

    class Meta:
        ordering = ['-created_time']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'pk': self.pk})

    def increase_views(self):
        self.views += 1
        self.save(update_fields=['views'])
