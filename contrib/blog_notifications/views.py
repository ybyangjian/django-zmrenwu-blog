from notifications.views import AllNotificationsList, UnreadNotificationsList

from blog.view_mixins import PaginationMixin
from braces.views import PrefetchRelatedMixin


class AllNotificationsListView(PaginationMixin, AllNotificationsList):
    paginate_by = 20
    prefetch_related = ('actor', 'target')


class UnreadNotificationsListView(PaginationMixin, UnreadNotificationsList):
    paginate_by = 20
    prefetch_related = ('actor', 'target')
