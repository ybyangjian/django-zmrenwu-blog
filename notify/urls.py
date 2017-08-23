from django.conf.urls import url

from . import views

app_name = 'notify'
urlpatterns = [
    url(r'^notifications/$', views.AllNotificationsListView.as_view(), name='notification_all'),
    url(r'^notifications/unread/$', views.UnreadNotificationsListView.as_view(), name='notification_unread'),
]
