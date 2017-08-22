class PaginationMixin(object):
    def get_pagination_context(self, paginator, page, is_paginated):
        if not is_paginated:
            return {}

        left, right = [], []
        left_has_more, right_has_more = False, False
        first, last = False, False
        page_number, page_range = page.number, paginator.page_range
        total_pages = paginator.num_pages

        if page_number == 1:
            right = page_range[page_number:page_number + 2]

            try:
                if right[-1] < total_pages - 1:
                    right_has_more = True
                    last = True
                elif right[-1] < total_pages:
                    last = True
            except IndexError:
                # IndexError means there is only one page
                right_has_more = False
                last = False

        elif page_number == total_pages:
            left = page_range[(page_number - 3) if (page_number - 3) > 0 else 0:page_number - 1]

            try:
                if left[0] > 2:
                    left_has_more = True
                    first = True
                elif left[0] > 1:
                    first = True
            except IndexError:
                # IndexError means there is only one page
                left_has_more = False
                first = False
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paginator = context.get('paginator')
        page = context.get('page_obj')
        is_paginated = context.get('is_paginated')
        context.update(self.get_pagination_context(paginator, page, is_paginated))
        return context
