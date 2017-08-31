from django.views.generic import View, DetailView, RedirectView
from django.views.generic.edit import FormMixin
from django.core.exceptions import ObjectDoesNotExist

from braces.views import SetHeadlineMixin

from .models import BlogComment
from .forms import BlogCommentForm

import django_comments as comments


class CommentReplyView(FormMixin, SetHeadlineMixin, DetailView):
    headline = '回复评论'
    model = BlogComment
    form_class = BlogCommentForm
    pk_url_kwarg = 'pid'
    template_name = 'comments/reply.html'

    def get_form_kwargs(self):
        kwargs = super(CommentReplyView, self).get_form_kwargs()
        kwargs.update({
            'target_object': self.object.content_object,
            'parent': self.object.pk
        })
        return kwargs


class CommentSuccess(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        self.url = self.comment.get_absolute_url()
        return super(CommentSuccess, self).get_redirect_url(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        self.comment = None
        if 'c' in request.GET:
            try:
                self.comment = comments.get_model().objects.get(
                    pk=request.GET['c'])
            except (ObjectDoesNotExist, ValueError):
                pass
        if self.comment and self.comment.is_public:
            return super(CommentSuccess, self).get(request, *args, **kwargs)
