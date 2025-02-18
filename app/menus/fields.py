from django.utils.translation import gettext_lazy as _

from wagtail.fields import StreamField

from menus.blocks import MenuCategoryBlock, MenuPageLinkItemBlock, MenuURLLinkBlock


def MenuItemStreamField(required=False, verbose_name=_("menu items")) -> StreamField:
    blank = not required

    return StreamField(
        [
            ("menu_category", MenuCategoryBlock()),
            ("page_link", MenuPageLinkItemBlock()),
            ("url_link", MenuURLLinkBlock()),
        ],
        verbose_name=verbose_name,
        blank=blank,
        use_json_field=True
    )
