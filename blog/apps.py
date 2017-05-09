from django.apps import AppConfig


class BlogConfig(AppConfig):
    name = 'blog'

    def ready(self):
        from comments.moderation import moderator
        from comments.moderation import BlogCommentModerator
        moderator.register(self.get_model('Post'), BlogCommentModerator)
