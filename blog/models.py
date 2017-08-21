import os
import markdown

from django.db import models
from django.db.models import Sum, Max
from django.conf import settings
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django.utils.html import strip_tags
from django.utils.six import python_2_unicode_compatible
from django.contrib.contenttypes.fields import GenericRelation

from model_utils import Choices
from model_utils.fields import AutoCreatedField, AutoLastModifiedField

from comments.models import BlogComment


class Tag(models.Model):
    name = models.CharField(_('name'), max_length=100)

    def __str__(self):
        return self.name


class Category(models.Model):
    GENRE_CHOICES = Choices(
        (1, 'collection', _('collection')),
        (2, 'tutorial', _('tutorial')),
    )

    STATUS_CHOICES = Choices(
        (1, 'ongoing', _('ongoing')),
        (2, 'finished', _('finished')),
    )

    name = models.CharField(_('name'), max_length=100)
    title = models.CharField(_('title'), max_length=255, blank=True)
    slug = models.SlugField(_('slug'), unique=True)
    description = models.TextField(_('description'), blank=True)
    created = models.DateTimeField(_('creation time'), auto_now_add=True)
    genre = models.PositiveSmallIntegerField(_('genre'), choices=GENRE_CHOICES,
                                             default=GENRE_CHOICES.collection)
    status = models.PositiveSmallIntegerField(_('status'), choices=STATUS_CHOICES, blank=True, null=True)
    cover = models.ImageField(_('cover'), upload_to='covers/categories/%Y/%m/%d/', blank=True)
    cover_caption = models.CharField(_('cover caption'), max_length=255, blank=True)
    resource = models.URLField(_('resource'), blank=True)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('creator'))

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.title:
            self.title = self.name

        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blog:category_slug', kwargs={'slug': self.slug})

    def total_views(self):
        if not self.post_set.exists():
            return {'category_views': 0}

        return self.post_set.aggregate(category_views=Sum('views'))

    def last_modified(self):
        return self.post_set.aggregate(last_modified=Max('modified_time'))


def post_cover_path(instance, filename):
    return os.path.join('posts', str(instance.pk), filename)


@python_2_unicode_compatible
class Post(models.Model):
    STATUS_CHOICES = Choices(
        (1, 'published', 'published'),
        (2, 'draft', 'draft'),
        (3, 'hidden', 'hidden'),
    )

    status = models.PositiveSmallIntegerField(_('status'), choices=STATUS_CHOICES, default=STATUS_CHOICES.draft)
    title = models.CharField(_('title'), max_length=255)
    body = models.TextField(_('body'))
    excerpt = models.CharField(_('excerpt'), max_length=255, blank=True)
    views = models.PositiveIntegerField(_('views'), default=0, editable=False)
    pub_date = models.DateTimeField(_('publication time'), blank=True, null=True)

    # Do not user auto_add=True or auto_now_add=True since value is None before instance be saved
    created_time = AutoCreatedField(_('creation time'))
    modified_time = AutoLastModifiedField(_('modification time'))
    cover = models.ImageField(_('cover'), upload_to=post_cover_path, blank=True)
    category = models.ForeignKey(Category, verbose_name=_('category'), null=True, blank=True)
    tags = models.ManyToManyField(Tag, verbose_name=_('tags'), blank=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('author'))
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
            # TODO: refactor and test
            self.excerpt = strip_tags(md.convert(self.body))[:74]

        if not self.pub_date and self.status == self.STATUS_CHOICES.published:
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
        # TODO: refactor and test
        return len(strip_tags(md.convert(self.body)))

    def is_tutorial(self):
        if not self.category:
            return False
        return self.category.get_genre_display() == 'tutorial'

    def root_comments(self):
        # TODO: move the logic to comment manager
        return self.comments.filter(parent__isnull=True, is_public=True, is_removed=False)
