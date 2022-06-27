import math


def make_pagination_range(page_range, page_qty, current_page):
    middle_range = math.ceil(page_qty / 2)  # math.ceil round the division up
    start_range = current_page - middle_range
    stop_range = current_page + middle_range
    total_pages = len(page_range)

    # Used if start range page is negative
    start_range_offset = abs(start_range) if start_range < 0 else 0  # Converts a negative number in a positive one

    # If the start range is less than 0 it is changed to 0 and 
    # the stop range sum with the start_range_offset.
    if start_range < 0:
        start_range = 0
        stop_range += start_range_offset

    if stop_range >= total_pages:
        start_range = start_range - abs(total_pages - stop_range)

    pagination = page_range[start_range:stop_range]

    return {
        'pagination': pagination,
        'page_range': page_range,
        'page_qty': page_qty,
        'current_page': current_page,
        'total_pages': total_pages,
        'start_range': start_range,
        'stop_range': stop_range,
        'first_page_out_of_range': current_page > middle_range,
        'last_page_out_of_range': stop_range < total_pages,
    }
