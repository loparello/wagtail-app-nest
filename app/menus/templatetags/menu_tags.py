from typing import Union

from django.template import Library

from wagtail.models import Page
from wagtail.blocks import StructValue

from menus.models import Menu
from menus.helpers import (
    get_menu_for_site,
    menu_item_page_is_active,
    menu_category_is_active,
    generate_submenu,
    get_active_class,
)
from menus.serializers import serialize_menu_to_dict


register = Library()


@register.inclusion_tag("menus/main_menu.html", takes_context=True)
def main_menu(context):
    request = context["request"]
    main_menu_context = {
        "request": request,
        "page": context.get("page"),
    }

    try:
        main_menu_context["main_menu"] = get_menu_for_site(request, main_menu=True)

    except Menu.DoesNotExist:
        main_menu_context["main_menu"] = None

    return main_menu_context


@register.simple_tag(takes_context=True)
def menu(context, handle):
    return get_menu_for_site(context["request"], handle=handle)


@register.simple_tag()
def page_submenu(menu_item: Union[StructValue, dict]) -> dict:
    def get_child_pages(menu_item):
        menu_item_page = menu_item.get("page")
        return list(menu_item_page.get_children().live().in_menu())

    return generate_submenu(menu_item, get_child_pages, "label_or_page_title")


@register.simple_tag(takes_context=True)
def menuitemactiveclass(
    context: dict, class_name: str, menu_item_page: Page = None, check_active_item=True
) -> str:
    if not check_active_item or not menu_item_page:
        return ""

    if not isinstance(menu_item_page, Page):
        return ""

    return get_active_class(context, class_name, menu_item_page_is_active, menu_item_page)


@register.simple_tag(takes_context=True)
def menucategoryactiveclass(
    context: dict,
    class_name: str,
    item: StructValue,
    check_active_item=True,
) -> str:
    if not check_active_item or not isinstance(item, StructValue):
        return ""

    return get_active_class(context, class_name, menu_category_is_active, item)


@register.simple_tag(takes_context=True)
def menutodict(
    context: dict,
    menu: Union[Menu, None] = None,
    handle: str = "",
    check_active_item: bool = False,
) -> dict:
    request = context["request"]
    current_page = context.get("page")
    selected_menu = None

    if menu:
        if not isinstance(menu, Menu):
            raise ValueError("menutodict tag expected a Menu object, got %r" % menu)

        selected_menu = menu
    elif handle:
        selected_menu = get_menu_for_site(request, handle=handle)

    if selected_menu:
        return serialize_menu_to_dict(menu, request, current_page, check_active_item)

    return {}
