from django.core.exceptions import ObjectDoesNotExist
from rest_framework.views import Response
from rest_framework.pagination import PageNumberPagination


class CustomPageNumberPagination(PageNumberPagination):
    page_size = 10  # number of items per page
    page_size_query_param = 'page_size'
    max_page_size = 100  # maximum number of items per page

    def get_page_size(self, request):
        data = request.GET.copy()
        page_size = data.get('page_size', None)

        if page_size is not None:
            try:
                page_size = int(page_size)
                if page_size < 1:
                    return self.page_size
                elif page_size > self.max_page_size:
                    return self.max_page_size
                else:
                    return page_size
            except ValueError:
                pass
        return self.page_size

    def get_paginated_response(self, data):
        return Response({
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'total_pages': self.page.paginator.num_pages,
            'current_page': self.page.number,
            'count': self.page.paginator.count,
            'data': data,
        })

    def get_paginated_response(self, data):
        return Response({
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'total_pages': self.page.paginator.num_pages,
            'current_page': self.page.number,
            'count': self.page.paginator.count,
            'data': data,
        })
