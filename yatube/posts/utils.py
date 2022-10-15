from django.core.paginator import Paginator


def paginator(posts, page_lim, request):
    pagin = Paginator(posts, page_lim)
    page_number = request.GET.get("page")

    return pagin.get_page(page_number)

