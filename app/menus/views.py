from django.utils.translation import gettext_lazy as _

from wagtail.admin.ui.tables import BooleanColumn
from wagtail.snippets.views.snippets import SnippetViewSet

from .models import Menu
from .panels import MenuPanels


class MenuViewSet(SnippetViewSet):
    model = Menu
    icon = "list-ul"
    menu_label = _("Menus")
    add_to_settings_menu = True
    menu_order = 900
    list_display = [
        "title",
        "handle",
        "site",
        BooleanColumn("is_main", label=_("Is main menu")),
    ]
    list_filter = ["site", "is_main"]
    search_fields = ["title", "handle"]

    panels = MenuPanels()
