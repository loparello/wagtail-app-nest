from django.utils.translation import gettext_lazy as _
from django.utils.functional import cached_property

from wagtail.blocks import (
    StructBlock,
    StructValue,
    StreamBlock,
    CharBlock,
    BooleanBlock,
    PageChooserBlock,
    URLBlock,
)

from nest.blocks import LabelBlock
from menus.helpers import (
    get_link_block_url,
    get_link_block_target,
    get_link_block_label,
    menu_category_has_submenu,
)


class MenuItemBlock(StructBlock):
    class Meta:
        icon = "link"
        label = _("Menu item")

    label = LabelBlock(
        required=True,
        default=None,
        help_text=_("The menu item label as it will be seen in the menu"),
    )
    handle = CharBlock(
        required=False,
        label=_("Handle"),
        max_length=100,
        help_text=_("Optional. Used to reference this menu item in templates etc."),
    )


class MenuLinkStructValue(StructValue):
    @cached_property
    def url(self):
        return get_link_block_url(self)

    @cached_property
    def target(self):
        return get_link_block_target(self)

    @cached_property
    def label_or_page_title(self):
        return get_link_block_label(self)


class MenuLinkBlock(MenuItemBlock):
    class Meta:
        label = _("Menu link")
        template = "menus/blocks/menu_link.html"
        value_class = MenuLinkStructValue

    open_external = BooleanBlock(
        required=False,
        label=_("Open in new tab"),
        help_text=_("If checked the link will open in a new browser tab"),
    )


class MenuPageLinkBlock(MenuLinkBlock):
    class Meta:
        label = _("Page link")

    label = LabelBlock(
        required=False,
        default=None,
        help_text=_(
            "Optional. If provided it will override the page title in the menu item"
        ),
    )
    page = PageChooserBlock(
        required=True,
        label=_("Page"),
        help_text=_("A link to an internal page of this site"),
    )
    url_addition = CharBlock(
        required=False,
        max_length=255,
        label=_("URL addition"),
        help_text=_(
            "Optional. A #hash or query string to append to the URL "
            "of the selected page"
        ),
    )


class MenuPageLinkItemBlock(MenuPageLinkBlock):
    add_submenu = BooleanBlock(
        required=False,
        label=_("Add submenu"),
        help_text=_(
            "If enabled, it will automatically generate a submenu from "
            "child pages of the menu item page which have the option "
            "'Show in menus' selected"
        ),
    )


class MenuURLLinkBlock(MenuLinkBlock):
    class Meta:
        icon = "link-external"
        label = _("URL link")

    url = URLBlock(required=True, help_text=_("A link to an custom url"))


class SubmenuBlock(StreamBlock):
    class Meta:
        template = "menus/blocks/submenu.html"

    page_link = MenuPageLinkBlock()
    url_link = MenuURLLinkBlock()


class MenuCategoryStructValue(StructValue):
    @cached_property
    def has_submenu(self):
        return menu_category_has_submenu(self)


class MenuCategoryBlock(MenuItemBlock):
    class Meta:
        icon = "list-ul"
        label = _("Menu category")
        template = "menus/blocks/menu_category.html"
        value_class = MenuCategoryStructValue
        help_text = _(
            "A menu category is a label that groups menu items together. "
            "It can be used to create a submenu with multiple links of "
            "different types."
        )

    submenu_items = SubmenuBlock(required=False)
