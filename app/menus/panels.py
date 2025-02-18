from django.utils.translation import gettext_lazy as _

from wagtail.admin.panels import FieldPanel, MultiFieldPanel


def MenuPanels() -> list:
    return [
        MultiFieldPanel(
            [
                FieldPanel(
                    "site",
                    help_text=_("The site this menu belongs to"),
                ),
                FieldPanel(
                    "title",
                    help_text=_("The title of the menu for internal reference"),
                ),
                FieldPanel(
                    "handle",
                    help_text=_(
                        "Used to reference this menu in templates etc. Must be unique "
                        "for the selected site. If not provided it will be automatically "
                        "generated from 'title'"
                    ),
                ),
                FieldPanel(
                    "heading",
                    help_text=_(
                        "Optional. The heading that will appear above the menu in "
                        "templates"
                    ),
                ),
            ],
            heading=_("Details"),
        ),
        MultiFieldPanel(
            [
                FieldPanel(
                    "is_main",
                    help_text=_(
                        "Sets this menu as the site main menu. There can be only one "
                        "per site"
                    ),
                ),
                FieldPanel(
                    "submenu_levels",
                    help_text=_(
                        "The number of levels of child pages to show in the submenus"
                    ),
                ),
            ],
            heading=_("Settings"),
        ),
        FieldPanel("menu_items"),
    ]
