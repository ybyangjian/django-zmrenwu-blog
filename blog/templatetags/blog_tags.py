from django import template
from django.template.loader import render_to_string
from django.conf import settings

from ..models import Post, Category

register = template.Library()


@register.simple_tag
def get_recent_posts(num=10):
    return Post.objects.all()[:num]


@register.simple_tag
def archives():
    return Post.objects.dates('created_time', 'month', order='DESC')


@register.simple_tag
def get_categories():
    return Category.objects.all()


@register.filter
def describe(obj):
    verb = obj.verb
    tmpl = getattr(settings, 'NOTIFICATION_TEMPLATES')[verb]
    context = {
        'notification': obj,
        'actor': obj.actor,
        'target': obj.target,
    }
    return render_to_string(tmpl, context=context)
