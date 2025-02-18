from django.utils.translation import gettext_lazy as _

from nest.blocks import (
    ImageBlock,
    TitleBlock,
    DescriptionBlock,
    LayoutChooserBlock,
)


class DetailBlock(LayoutChooserBlock):
    """A repeatable struct block with title, descripion, image and layout choice"""

    class Meta:
        template = "flexiblepages/blocks/detail.html"
        icon = "form"
        label = _("Detail")
        help_text = _(
            "A block of content with title, descripion and image "
            "to display a featured detail. Text can be positioned "
            "left or right of the image"
        )

    title = TitleBlock(required=True)
    description = DescriptionBlock(required=True)
    image = ImageBlock(required=True)
