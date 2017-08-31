from django.utils.translation import ugettext_lazy as _

from django_comments.abstracts import CommentAbstractModel
from django_comments.managers import CommentManager
from mptt.managers import TreeManager
from mptt.models import MPTTModel, TreeForeignKey


class BlogCommentManager(TreeManager, CommentManager):
    pass


class BlogComment(MPTTModel, CommentAbstractModel):
    parent = TreeForeignKey('self', null=True, blank=True,
                            related_name='children', verbose_name=_('parent comment'))
    objects = BlogCommentManager()

    class Meta(CommentAbstractModel.Meta):
        pass

    class MPTTMeta:
        order_insertion_by = ['-submit_date']

    def get_descendants_reversely(self):
        return self.get_descendants().order_by('submit_date')
