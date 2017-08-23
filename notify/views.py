from notifications.views import AllNotificationsList, UnreadNotificationsList

from blog.view_mixins import PaginationMixin


class AllNotificationsListView(PaginationMixin, AllNotificationsList):
    paginate_by = 20
    prefetch_related = ('actor', 'target')


class UnreadNotificationsListView(PaginationMixin, UnreadNotificationsList):
    paginate_by = 20
    prefetch_related = ('actor', 'target')
