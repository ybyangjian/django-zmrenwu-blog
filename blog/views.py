import markdown
from markdown.extensions.toc import TocExtension

from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Count
from django.utils.text import slugify
from django.views.generic import ListView, DetailView

from notifications.views import AllNotificationsList, UnreadNotificationsList

from blog.models import Post, Category
from .view_mixins import PaginationMixin

from braces.views import SelectRelatedMixin


class IndexView(PaginationMixin, SelectRelatedMixin, ListView):
    model = Post
    paginate_by = 10
    template_name = 'blog/index.html'
    select_related = ('author', 'category')

    def get_queryset(self):
        return super().get_queryset().annotate(comment_count=Count('comments'))


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'
    context_object_name = 'post'

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        self.object.increase_views()
        return response

    def get_object(self, queryset=None):
        post = super().get_object(queryset=None)
        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            TocExtension(slugify=slugify),
        ])
        post.body = md.convert(post.body)
        post.toc = md.toc

        return post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.object

        try:
            previous_post = post.get_previous_by_created_time()
        except Post.DoesNotExist:
            previous_post = None

        try:
            next_post = post.get_next_by_created_time()
        except Post.DoesNotExist:
            next_post = None

        if post.category.genre == Category.GENRE_CHOICES.tutorial:
            self.template_name = 'blog/tutorial.html'
            post_list = post.category.post_set.all().order_by('created_time')
            context['post_list'] = post_list

        context['previous_post'] = previous_post
        context['next_post'] = next_post

        return context


def category(request, pk):
    cate = get_object_or_404(Category, pk=pk)
    return redirect(cate, permanent=True)


class CategoryPostListView(IndexView):
    template_name = 'blog/category.html'

    def get_queryset(self):
        cate = get_object_or_404(Category, slug=self.kwargs.get('slug'))
        qs = super().get_queryset()
        post_list = qs.filter(category=cate)

        if cate.genre == Category.GENRE_CHOICES.tutorial:
            post_list = post_list.order_by('created_time')
            self.template_name = 'blog/tutorial.html'
            self.paginate_by = None

        return post_list

    def get_context_data(self, **kwargs):
        cate = get_object_or_404(Category, slug=self.kwargs.get('slug'))
        context = super().get_context_data(**kwargs)
        context['category'] = cate

        return context


class TutorialListView(ListView):
    model = Category
    template_name = 'blog/tutorial_list.html'
    context_object_name = 'tutorial_list'

    # TODO: refactor to manager
    queryset = Category.objects.filter(genre=Category.GENRE_CHOICES.tutorial)


class CategoryListView(ListView):
    model = Category
    template_name = 'blog/category_list.html'

    # TODO: refactor to manager
    queryset = Category.objects.exclude(genre=Category.GENRE_CHOICES.tutorial)


class PostArchivesView(ListView):
    model = Post
    template_name = 'blog/archives.html'


class AllNotificationsListView(PaginationMixin, AllNotificationsList):
    paginate_by = 20


class UnreadNotificationsListView(PaginationMixin, UnreadNotificationsList):
    paginate_by = 20
