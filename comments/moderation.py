from django_comments.moderation import CommentModerator, Moderator
from notifications.signals import notify


class BlogModerator(Moderator):
    def post_save_moderation(self, sender, comment, request, **kwargs):
        model = comment.content_type.model_class()
        if model not in self._registry:
            return
        self._registry[model].reply(comment, comment.content_object, request)


class BlogCommentModerator(CommentModerator):
    def reply(self, comment, content_object, request):
        # 通知文章作者,如果是文章作者自己评论，则不通知
        post_author = content_object.author
        if post_author != comment.user:
            comment_data = {
                'recipient': post_author,
                'verb': 'comment',
                'target': comment,
            }
            notify.send(sender=comment.user, **comment_data)

        # 通知被评论的人
        if comment.parent:
            parent_user = comment.parent.user
            # 自己回复自己无需通知
            if parent_user != comment.user:
                reply_data = {
                    'recipient': parent_user,
                    'verb': 'reply',
                    'target': comment,
                }
                notify.send(sender=comment.user, **reply_data)

moderator = BlogModerator()
