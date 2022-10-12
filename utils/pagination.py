import math

from django.core.paginator import EmptyPage, InvalidPage, Paginator


def make_pagination_range(page_range,
                          qty_pages,
                          current_page):
    midle_range = math.ceil(qty_pages/2)
    start_range = current_page-midle_range
    stop_range = current_page+midle_range

    if start_range < 0:
        stop_range = stop_range + abs(start_range)
        start_range = 0
    total_pages = len(page_range)
    if stop_range >= total_pages:
        start_range = start_range - abs(total_pages-stop_range)
    pagination = page_range[start_range:stop_range]
    return {
        'pagination': pagination,
        'page_range': page_range,
        'qty_pages': qty_pages,
        'current_page': current_page,
        'total_pages': total_pages,
        'start_range': start_range,
        'stop_range': stop_range,
        'first_page_out_of_range': current_page > midle_range,
        'last_page_out_of_range': stop_range < total_pages
    }


def make_pagination(request, recipes, perpage, qty_pages=4):
    try:
        current_page = int(request.GET.get('page', 1))
    except ValueError:
        current_page = 1
    paginator = Paginator(object_list=recipes, per_page=perpage)
    page_obj = paginator.get_page(current_page)

    pagination_range = make_pagination_range(
        page_range=paginator.page_range,
        qty_pages=qty_pages,
        current_page=current_page
    )
    return page_obj, pagination_range
