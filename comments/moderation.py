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
        post_author = content_object.author

        if comment.parent:
            parent_user = comment.parent.user
            # 通知被评论的人，自己回复自己无需通知
            if parent_user != comment.user:
                reply_data = {
                    'recipient': parent_user,
                    'verb': 'reply',
                    'target': comment,
                }
                notify.send(sender=comment.user, **reply_data)

            if parent_user != content_object.author and post_author != comment.user:
                # 如果被回复的人不是文章作者，且不是文章作者自己的回复，文章作者应该收到通知
                comment_data = {
                    'recipient': post_author,
                    'verb': 'comment',
                    'target': comment,
                }
                notify.send(sender=comment.user, **comment_data)
        else:
            # 如果是直接评论，且不是文章作者自己评论，则通知文章作者
            if post_author != comment.user:
                comment_data = {
                    'recipient': post_author,
                    'verb': 'comment',
                    'target': comment,
                }
                notify.send(sender=comment.user, **comment_data)


moderator = BlogModerator()
