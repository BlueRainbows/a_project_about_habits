from rest_framework.pagination import PageNumberPagination


class PaginationHabits(PageNumberPagination):
    """
    Создание пагинации из 5ти объектов в одной странице.
    Определён параметр page_size.
    Максимальный размер страницы 25.
    """
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 25
