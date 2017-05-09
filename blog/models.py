import os
import markdown

from django.db import models
from django.db.models import Sum, Max
from django.conf import settings
from django.urls import reverse
from django.utils.html import strip_tags
from django.utils.six import python_2_unicode_compatible
from django.contrib.contenttypes.fields import GenericRelation

from comments.models import BlogComment


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
    created = models.DateTimeField(auto_now_add=True)
    genre = models.PositiveSmallIntegerField(choices=GENRE_CHOICES)
    status = models.PositiveSmallIntegerField(choices=STATUS_CHOICES, blank=True, null=True)
    cover = models.ImageField(upload_to='covers/categories/%Y/%m/%d/', blank=True)
    cover_caption = models.CharField(max_length=255, blank=True)
    resource = models.URLField(blank=True)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.title:
            self.title = self.name

        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blog:category_slug', kwargs={'slug': self.slug})

    def total_views(self):
        return self.post_set.aggregate(category_views=Sum('views'))

    def last_modified(self):
        return self.post_set.aggregate(last_modified=Max('modified_time'))


def post_cover_path(instance, filename):
    return os.path.join('posts', str(instance.pk), filename)


@python_2_unicode_compatible
class Post(models.Model):
    STATUS_CHOICES = (
        (1, 'published'),
        (2, 'draft'),
        (3, 'hidden'),
    )

    status = models.PositiveSmallIntegerField(choices=STATUS_CHOICES)
    title = models.CharField(max_length=255)
    body = models.TextField()
    excerpt = models.CharField(max_length=255, blank=True)
    views = models.PositiveIntegerField(default=0, editable=False)
    pub_date = models.DateTimeField(blank=True, null=True)
    created_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)
    cover = models.ImageField(upload_to=post_cover_path, blank=True)
    category = models.ForeignKey(Category, null=True, blank=True)
    tags = models.ManyToManyField(Tag, blank=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    comments = GenericRelation(BlogComment, object_id_field='object_pk', content_type_field='content_type')

    class Meta:
        ordering = ['-created_time']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.excerpt:
            md = markdown.Markdown(extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',
            ])
            self.excerpt = strip_tags(md.convert(self.body))[:74]

        if not self.pub_date and self.get_status_display() == 'published':
            self.pub_date = self.created_time

        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'pk': self.pk})

    def increase_views(self):
        self.views += 1
        self.save(update_fields=['views'])

    def word_count(self):
        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
        ])
        return len(strip_tags(md.convert(self.body)))

    def is_tutorial(self):
        if not self.category:
            return False
        return self.category.get_genre_display() == 'tutorial'

    def root_comments(self):
        return self.comments.filter(parent__isnull=True, is_public=True, is_removed=False)
