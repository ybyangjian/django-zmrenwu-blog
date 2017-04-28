from django.db import models
from django.conf import settings
from django.utils.six import python_2_unicode_compatible
from django.urls import reverse


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


@python_2_unicode_compatible
class Post(models.Model):
    title = models.CharField(max_length=70)
    body = models.TextField()
    created_time = models.DateTimeField()
    modified_time = models.DateTimeField()
    excerpt = models.CharField(max_length=200, blank=True)
    category = models.ForeignKey(Category, blank=True, null=True)
    tags = models.ManyToManyField(Tag, blank=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL)

    class Meta:
        ordering = ['-created_time']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'pk': self.pk})
