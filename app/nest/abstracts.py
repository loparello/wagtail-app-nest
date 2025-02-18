from django.db import models
from django.utils.translation import gettext_lazy as _

from wagtail.models import Page
from wagtail.admin.panels import (
    FieldPanel,
    PageChooserPanel,
    MultiFieldPanel,
    TitleFieldPanel,
)

from nest.fields import (
    WagtailPageField,
    LabelField,
    PageHeroImageField,
)


class BasePage(Page):
    """The base model for pages to extend the Wagtail Page model"""

    class Meta:
        abstract = True

    # Override in page models to add a user friendly description of the page type
    page_description = "A page"

    image = PageHeroImageField()

    search_fields = Page.search_fields

    # TitleFieldPanel is used to connect the slug field to the title field.
    # When the title field is edited, the slug field is automatically updated.
    # This is useful for creating a unique URL for the page.
    # https://docs.wagtail.org/en/stable/reference/pages/panels.html#titlefieldpanel
    content_panels = [
        MultiFieldPanel(
            [TitleFieldPanel("title"), FieldPanel("image")],
            heading=_("Title and image"),
        ),
    ]


class BaseExternalLink(models.Model):
    """
    Abstract model for external link items,
    To use mostly with Wagtail orderable models
    """

    class Meta:
        abstract = True
        verbose_name = _("External link")
        verbose_name_plural = _("External links")

    label = LabelField(required=True)
    url = models.URLField(
        _("URL"),
        max_length=255,
        blank=False,
    )
    slug = models.SlugField(
        unique=True,
        max_length=100,
        blank=True,
        help_text=_(
            "Optional. The tag that will be used in the HTML "
            "to reference this external link (e.g. To display "
            "a related icon or image). Recommended: e.g. "
            'if label is "Facebook" set slug as "facebook". '
            "It must be unique"
        ),
    )

    panels = [
        FieldPanel("label"),
        FieldPanel("url"),
        FieldPanel("slug"),
    ]

    def __str__(self):
        return self.label


class BasePageChooser(models.Model):
    """
    Abstract model for page chooser items.
    To use mostly with Wagtail orderable models
    """

    class Meta:
        abstract = True

    page = WagtailPageField(
        required=True,
        on_delete=models.CASCADE,
        verbose_name=_("page"),
    )

    panels = [PageChooserPanel("page")]

    def __str__(self):
        return self.page.title
