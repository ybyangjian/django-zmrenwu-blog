from django.conf.urls import url

from . import views

app_name = 'blog'
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^popular/$', views.PopularPostListView.as_view(), name='popular'),
    url(r'^post/(?P<pk>[0-9]+)/$', views.PostDetailView.as_view(), name='detail'),
    url(
        r'^category/django-advanced-blog-tutorial/$',
        views.django_advanced_blog_tutorial_redirect
    ),
    url(r'^category/(?P<pk>[0-9]+)/$', views.category, name='category'),
    url(
        r'^category/(?P<slug>[-_\w]+)/$',
        views.CategoryPostListView.as_view(),
        name='category_slug'),
    url(r'^tutorials/$', views.TutorialListView.as_view(), name='tutorials'),
    url(r'^categories/$', views.CategoryListView.as_view(), name='categories'),
    url(r'^archives/$', views.PostArchivesView.as_view(), name='archives'),
    url(r'^donate/$', views.DonateView.as_view(), name='donate'),
]
