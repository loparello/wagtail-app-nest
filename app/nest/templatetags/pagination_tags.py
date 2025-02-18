from django.template import Library


register = Library()


@register.inclusion_tag("nest/partials/_pagination_nav.html")
def pagination_nav(request, page_item, page_limit=8, num_edge_pages=3):
    edge_page_range = []
    end_edge_page_num = page_item.paginator.num_pages - (num_edge_pages - 1)

    context = {
        "request": request,
        "page_item": page_item,
        "edge_page_range": edge_page_range,
        "start_edge_page_num": num_edge_pages,
        "end_edge_page_num": end_edge_page_num,
        "above_page_limit": False,
    }

    if page_item.paginator.num_pages > page_limit:
        context["above_page_limit"] = True

        if page_item.number <= num_edge_pages:
            for page_num in page_item.paginator.page_range:
                if page_num > 1 and page_num <= num_edge_pages:
                    edge_page_range.append(page_num)
        elif page_item.number >= end_edge_page_num:
            for page_num in page_item.paginator.page_range:
                if (
                    page_num >= end_edge_page_num
                    and page_num < page_item.paginator.num_pages
                ):
                    edge_page_range.append(page_num)

    return context
