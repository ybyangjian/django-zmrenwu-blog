import markdown
from markdown.extensions.toc import TocExtension

from django.shortcuts import render, get_object_or_404, redirect
from django.utils.text import slugify
from django.views.generic import ListView

from .models import Post, Category


class PaginationMixin(object):
    def page_left_right(self, paginator, page, is_paginated):
        left = []
        right = []
        left_has_more = False
        right_has_more = False
        first = False
        last = False

        context = {
            'left': left,
            'right': right,
            'left_has_more': left_has_more,
            'right_has_more': right_has_more,
            'first': first,
            'last': last,
        }

        if not is_paginated:
            return context

        page_number = page.number
        total_pages = paginator.num_pages
        page_range = paginator.page_range

        if page_number == 1:
            right = page_range[page_number:page_number + 2]
            if right[-1] < total_pages - 1:
                right_has_more = True

            if right[-1] < total_pages:
                last = True
        elif page_number == total_pages:
            left = page_range[(page_number - 3) if (page_number - 3) > 0 else 0:page_number - 1]
            if left[0] > 2:
                left_has_more = True

            if left[0] > 1:
                first = True
        else:
            left = page_range[(page_number - 3) if (page_number - 3) > 0 else 0:page_number - 1]
            right = page_range[page_number:page_number + 2]
            if right[-1] < total_pages - 1:
                right_has_more = True
            if right[-1] < total_pages:
                last = True

            if left[0] > 2:
                left_has_more = True
            if left[0] > 1:
                first = True

        context = {
            'left': left,
            'right': right,
            'left_has_more': left_has_more,
            'right_has_more': right_has_more,
            'first': first,
            'last': last,
        }

        return context


class IndexView(ListView, PaginationMixin):
    model = Post
    paginate_by = 10
    template_name = 'blog/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paginator = context.get('paginator')
        page = context.get('page_obj')
        is_paginated = context.get('is_paginated')
        context.update(self.page_left_right(paginator, page, is_paginated))
        return context


def detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.increase_views()
    md = markdown.Markdown(extensions=[
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',
        TocExtension(slugify=slugify)
    ])
    post.body = md.convert(post.body)
    try:
        previous_post = post.get_previous_by_created_time()
    except Post.DoesNotExist:
        previous_post = None

    try:
        next_post = post.get_next_by_created_time()
    except Post.DoesNotExist:
        next_post = None

    return render(request, 'blog/detail.html', context={'post': post,
                                                        'toc': md.toc,
                                                        'previous_post': previous_post,
                                                        'next_post': next_post})


def archives(request, year, month):
    post_list = Post.objects.filter(created_time__year=year, created_time__month=month)
    return render(request, 'blog/index.html', context={'post_list': post_list})


def category(request, pk):
    cate = get_object_or_404(Category, pk=pk)
    return redirect(cate, permanent=True)


class CategoryView(ListView, PaginationMixin):
    paginate_by = 10
    template_name = 'blog/category.html'

    def get_queryset(self):
        cate = get_object_or_404(Category, slug=self.kwargs.get('slug'))
        post_list = cate.post_set.all()

        if cate.get_genre_display() == 'tutorial':
            post_list = post_list.order_by('created_time')
            self.template_name = 'blog/tutorial.html'
            self.paginate_by = None

        return post_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cate = get_object_or_404(Category, slug=self.kwargs.get('slug'))
        paginator = context.get('paginator')
        page = context.get('page_obj')
        is_paginated = context.get('is_paginated')
        context.update(self.page_left_right(paginator, page, is_paginated))
        context['category'] = cate
        return context


def category_slug(request, slug):
    cate = get_object_or_404(Category, slug=slug)
    post_list = Post.objects.filter(category=cate)

    if cate.get_genre_display() == 'tutorial':
        post_list = post_list.order_by('created_time')
        return render(request, 'blog/tutorial.html', context={'post_list': post_list,
                                                              'category': cate})
    return render(request, 'blog/category.html', context={'post_list': post_list,
                                                          'category': cate})
