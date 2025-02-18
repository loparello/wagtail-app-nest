from typing import Union

from django.db.models import Model
from django.apps import apps

from wagtail.models import Site, Page
from wagtail.blocks import StructValue


def get_menu_for_site(
    request: object, handle: str = "", main_menu: bool = False
) -> Union[Model, None]:
    Menu = apps.get_model("menus", "Menu")
    site = Site.find_for_request(request)

    if main_menu:
        try:
            return Menu.objects.get(is_main=True, site=site)
        except Menu.DoesNotExist:
            return None

    try:
        return Menu.objects.get(handle=handle, site=site)
    except Menu.DoesNotExist:
        return None


def get_link_block_url(value: StructValue) -> str:
    url = value.get("url")
    page = value.get("page")
    url_addition = value.get("url_addition")

    if url:
        return url

    if page:
        if url_addition:
            return page.url + url_addition

        return page.url

    return "#"


def get_link_block_target(value: StructValue) -> str:
    open_external = value.get("open_external")

    if open_external:
        return "_blank"

    return "_self"


def get_link_block_label(value: StructValue) -> str:
    label = value.get("label")
    page = value.get("page")

    if label:
        return label

    if page:
        return page.title

    return ""


def menu_category_has_submenu(value: StructValue) -> bool:
    submenu_items = value.get("submenu_items")

    if submenu_items:
        return len(submenu_items) > 0

    return False


def page_is_active(page: Page, current_page: Page) -> bool:
    return current_page.id == page.id or current_page.is_descendant_of(page)


def menu_item_page_is_active(menu_item_page: Page, current_page: Page) -> bool:
    if not menu_item_page or not current_page:
        return False
    return page_is_active(menu_item_page, current_page)


def menu_category_is_active(value: StructValue, current_page: Page) -> bool:
    if not value or not current_page:
        return False

    category_items = value.get("submenu_items")

    for item in category_items:
        page = item.value.get("page")
        if page and page_is_active(page, current_page):
            return True

    return False


def get_active_class(
    context: dict,
    class_name: str,
    check_active_func: callable,
    *args,
) -> str:
    return class_name if check_active_func(*args, context.get("page")) else ""


def generate_submenu(
    menu_item: Union[StructValue, dict],
    get_child_pages_func: callable,
    label_attr: str,
) -> dict:
    submenu = {"parent_menu_item": None, "submenu_items": []}

    if not menu_item or (hasattr(menu_item, "page") and not menu_item.get("add_submenu")):
        return submenu

    parent_menu_item = {
        "label": getattr(menu_item, label_attr, "") or menu_item.get("title", ""),
        "page": menu_item.get("page"),
        "category": menu_item.get("category"),
    }

    child_pages = get_child_pages_func(menu_item)
    if not child_pages:
        return submenu

    submenu_items = [
        {"label": child_page.title, "page": child_page} for child_page in child_pages
    ]

    submenu["parent_menu_item"] = parent_menu_item
    submenu["submenu_items"] = submenu_items

    return submenu
