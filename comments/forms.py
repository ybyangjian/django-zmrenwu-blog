from django import forms
from django.utils.translation import ugettext_lazy as _

from django_comments.forms import CommentForm
from django_comments.forms import COMMENT_MAX_LENGTH

from . import get_model
from .widgets import SimditorTextarea


class BlogCommentForm(CommentForm):
    parent = forms.IntegerField(required=False, widget=forms.HiddenInput)
    comment = forms.CharField(label=_('Comment'), widget=SimditorTextarea,
                              max_length=COMMENT_MAX_LENGTH)

    def __init__(self, target_object, parent=None, data=None, initial=None, **kwargs):
        self.parent = parent
        if initial is None:
            initial = {}
        initial.update({'parent': self.parent})
        super().__init__(target_object, data=data, initial=initial, **kwargs)
        self.fields['email'].required = False
        print(self.fields['parent'].value)

    def get_comment_model(self):
        return get_model()

    def get_comment_create_data(self, **kwargs):
        d = super().get_comment_create_data()
        d['parent_id'] = self.cleaned_data['parent']
        return d
