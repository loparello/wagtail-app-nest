from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from nest.fields import ForeignKeyField, TitleField, ChoiceField
from nest.helpers import get_unique_slug
from menus.fields import MenuItemStreamField


class BaseMenu(models.Model):
    """Abstract model for site menus"""

    class Meta:
        abstract = True
        unique_together = ("site", "handle")
        verbose_name = _("menu")
        verbose_name_plural = _("menus")

    SUBMENU_LEVEL_CHOICES = [
        (1, "1"),
        (2, "2"),
    ]

    site = ForeignKeyField(
        "wagtailcore.Site",
        verbose_name=_("site"),
        required=True,
        on_delete=models.CASCADE,
    )
    title = TitleField(
        required=True,
    )
    handle = models.SlugField(
        verbose_name=_("handle"),
        max_length=100,
        blank=True,
    )
    is_main = models.BooleanField(
        verbose_name=_("is main menu"),
        default=False,
    )
    menu_items = MenuItemStreamField(required=True)
    heading = TitleField(
        required=False,
        verbose_name=_("heading"),
    )
    submenu_levels = ChoiceField(
        SUBMENU_LEVEL_CHOICES,
        verbose_name=_("submenu levels"),
        required=True,
        is_numeric=True,
    )

    def __str__(self):
        return self.title

    def clean(self, *args, **kwargs):
        if not self.handle:
            self.handle = get_unique_slug(
                self, "title", "handle", limits={"site": self.site}
            )

        if self.is_main:
            site_main_menu = (
                self.__class__.objects.filter(is_main=True, site=self.site)
                .exclude(pk=self.pk)
                .first()
            )

            if site_main_menu:
                raise ValidationError(
                    {
                        "main": _("There is already a main menu for this site"),
                    }
                )
