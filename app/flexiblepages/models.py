from django.utils.translation import gettext_lazy as _

from wagtail.admin.panels import FieldPanel

from nest.abstracts import BasePage
from nest.mixins import PageIntroMixin, PageLinkMixin
from flexiblepages.fields import ContentStreamField


class FlexiblePage(BasePage, PageIntroMixin, PageLinkMixin):
    """A multi-purpose display page"""

    class Meta:
        verbose_name = _("Flexible Page")
        verbose_name_plural = _("Flexible Pages")

    page_description = "A multi-purpose page with modular content"
    parent_page_types = [
        "home.HomePage",
        "flexiblepages.FlexiblePage",
    ]
    subpage_types = ["flexiblepages.FlexiblePage"]

    content = ContentStreamField(required=True)

    search_fields = (
        BasePage.search_fields
        + PageIntroMixin.search_fields
        + PageLinkMixin.search_fields
    )

    content_panels = (
        BasePage.content_panels
        + PageIntroMixin.panels
        + PageLinkMixin.panels
        + [
            FieldPanel("content"),
        ]
    )
