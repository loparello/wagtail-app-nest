from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.functional import cached_property

from wagtail.admin.panels import (
    FieldPanel,
    MultiFieldPanel,
)
from wagtail.search import index

from nest.fields import TitleField, DescriptionField, ExcerptField


class PageIntroMixin(models.Model):
    """
    Adds subtitle and description fields to a page.
    To be used together with nest.abstracts.BasePage
    """

    class Meta:
        abstract = True

    subtitle = TitleField(
        verbose_name=_("subtitle"),
    )
    description = DescriptionField(
        verbose_name=_("description"),
    )

    search_fields = [
        index.AutocompleteField("subtitle"),
        index.AutocompleteField("description"),
    ]

    panels = [
        MultiFieldPanel(
            [
                FieldPanel(
                    "subtitle",
                    help_text=_("Optional. Additional text for the main heading"),
                ),
                FieldPanel(
                    "description",
                    help_text=_("Optional. The main description or introduction"),
                ),
            ],
            heading=_("Introduction"),
            help_text=_("An optional subtitle and description for the page"),
        ),
    ]

    @cached_property
    def has_intro(self):
        return True if self.subtitle or self.description else False


class PageLinkMixin(models.Model):
    """
    Adds link title and excerpt fields to a page.
    To be used together with nest.abstracts.BasePage
    """

    class Meta:
        abstract = True

    link_title = TitleField(
        verbose_name=_("link title"),
    )
    excerpt = ExcerptField()

    search_fields = [
        index.AutocompleteField("link_title"),
        index.AutocompleteField("excerpt"),
    ]

    panels = [
        MultiFieldPanel(
            [
                FieldPanel(
                    "link_title",
                    help_text=_(
                        "Optional. An alternative title to be used in place "
                        "of the main title in previews and links"
                    ),
                ),
                FieldPanel("excerpt"),
            ],
            heading=_("Previews and links"),
            help_text=_(
                "An alternative title and an excerpt for previews and links "
                "to the the page"
            ),
        ),
    ]

    @cached_property
    def has_preview(self):
        return True if self.link_title or self.excerpt else False


class PaginationSettingMixin(models.Model):
    """
    Common pagination settings for listings.
    Add the pannel to page settings tab
    """

    class Meta:
        abstract = True

    num_items_per_page = models.PositiveSmallIntegerField(
        _("Number of items per page"),
        default=10,
    )

    panels = [
        MultiFieldPanel(
            [
                FieldPanel(
                    "num_items_per_page",
                    help_text=_(
                        "The number of listed items to display at once in the page"
                    ),
                ),
            ],
            heading=_("Pagination"),
            help_text=_("Settings related to the pagination of list of items."),
        )
    ]
