from django.utils.translation import gettext_lazy as _
from wagtail.blocks import (
    BlockQuoteBlock,
    CharBlock,
    ChoiceBlock,
    PageChooserBlock,
    RichTextBlock,
    StreamBlock,
    StructBlock,
    StructValue,
    TextBlock,
    URLBlock,
)
from wagtail.embeds.blocks import EmbedBlock
from wagtail.images.blocks import ImageChooserBlock


def RichParagraphBlock(
    required=False,
    template="nest/blocks/rich_text.html",
    label=_("Paragraph"),
    icon="pilcrow",
    help_text=_("Rich text with headings, paragraph formatting, lists and links"),
) -> RichTextBlock:
    """Wrapper function around rich text block class with all text formatting elements"""
    return RichTextBlock(
        template=template,
        required=required,
        label=label,
        icon=icon,
        features=[
            "h2",
            "h3",
            "h4",
            "h5",
            "h6",
            "bold",
            "italic",
            "ol",
            "ul",
            "hr",
            "link",
        ],
        help_text=help_text,
    )


def TitleBlock(
    required=False,
    max_length=255,
    label=_("Title"),
    help_text=_("The title as it will be seen by the public"),
) -> CharBlock:
    """Wrapper function around a CharBlock specific for titles"""
    return CharBlock(
        required=required, max_length=max_length, label=label, help_text=help_text
    )


def LabelBlock(
    required=False,
    default=_("Read more"),
    max_length=100,
    label=_("Label"),
    help_text=_("A label as it will be seen by the public"),
) -> CharBlock:
    """Wrapper function around a CharBlock specific for labels"""
    return CharBlock(
        required=required,
        default=default,
        max_length=max_length,
        label=label,
        help_text=help_text,
    )


def DescriptionBlock(
    richtext=False,
    required=False,
    label=_("Description"),
    icon="pilcrow",
    help_text=_("A description as it will be seen by the public"),
) -> TextBlock:
    """Wrapper function to get descriptions as either TextBlock or RichTextBlock"""
    if richtext:
        return RichParagraphBlock(
            required=required,
            label=label,
            icon=icon,
            help_text=help_text,
        )

    return TextBlock(required=required, label=label, help_text=help_text)


def ImageBlock(
    required=False,
    template="nest/blocks/image.html",
    label=_("Image"),
    icon="image",
    help_text=_("An image to display. It is recommended a minimum width of 1140px"),
) -> ImageChooserBlock:
    """Wrapper function around image chooser block"""
    return ImageChooserBlock(
        template=template, required=required, label=label, icon=icon, help_text=help_text
    )


def VideoEmbedBlock(
    required=False,
    template="nest/blocks/video_embed.html",
    label=_("Video embed"),
    icon="media",
    help_text=_("A video embed. Insert a YouTube or Vimeo video link"),
) -> EmbedBlock:
    """Wrapper function around embed block"""
    return EmbedBlock(
        template=template, required=required, label=label, icon=icon, help_text=help_text
    )


class QuoteBlock(StructBlock):
    """An quotation with author block"""

    class Meta:
        template = "nest/blocks/quote.html"
        icon = "openquote"
        label = _("Quote")

    quote = BlockQuoteBlock(
        required=True, label=_("Quote"), max_length=255, help_text=_("The quotation text")
    )
    author = CharBlock(
        required=False,
        max_length=255,
        label=_("Author"),
        help_text=_("Optional. The name of the author the quote is taken from"),
    )


class ImageWithCaptionBlock(StructBlock):
    """An image with optional caption block"""

    class Meta:
        template = "nest/blocks/image_with_caption.html"
        icon = "image"
        label = _("Image with caption")

    image = ImageBlock(required=True, help_text=_("The image to display in the figure"))
    caption = TextBlock(
        required=False, label=_("Caption"), help_text=_("Optional. The image caption")
    )


class BodyTextBlock(StreamBlock):
    """A body text block with basic options"""

    class Meta:
        template = "nest/blocks/body_text.html"
        label = _("Body text")
        icon = "edit"
        help_text = _("Body text with paragraphs and quotes")

    paragraph = RichParagraphBlock()
    quote = QuoteBlock()


class BodyTextWithMediaBlock(BodyTextBlock):
    """A body text block with image and video sub-blocks"""

    class Meta:
        label = _("Body text with media")
        help_text = _("Body text with paragraphs, quotes, images and videos")

    image_with_caption = ImageWithCaptionBlock()
    video_embed = VideoEmbedBlock()


class LayoutChooserBlock(StructBlock):
    """A left or right layout chooser struct block"""

    layout = ChoiceBlock(
        choices=[
            ("left", "Left"),
            ("right", "Right"),
        ],
        required=True,
        default="left",
        help_text=_(
            "The text alignment. Select to have the text content "
            "positioned to left or right"
        ),
    )


class LinkStructValue(StructValue):
    def url(self):
        url = self.get("url")
        page = self.get("page")

        if url:
            return url
        if page:
            return page.url
        return "#"

    def target(self):
        url = self.get("url")

        if url:
            return "_blank"

        return "_self"


class BaseLinkBlock(StructBlock):
    """A base link block. Link type is defined in sub-classes"""

    class Meta:
        icon = "link"
        label = _("Link")
        value_class = LinkStructValue


class PageLinkBlock(BaseLinkBlock):
    """A link block that uses a page chooser"""

    class Meta:
        label = _("Page link")

    page = PageChooserBlock(
        required=True, help_text=_("A link to another page of this website")
    )


class URLLinkBlock(BaseLinkBlock):
    """A link block that uses a url field"""

    class Meta:
        icon = "link-external"
        label = _("URL link")

    url = URLBlock(required=True, help_text=_("A link to an specific url"))


class LinkStreamBlock(StreamBlock):
    class Meta:
        label = _("Link")
        icon = "link"
        max_num = 1
        help_text = _("Add a link to a page of this website or to a specific URL")

    page_link = PageLinkBlock()
    url_link = URLLinkBlock()


class CallToActionLinkBlock(StructBlock):
    class Meta:
        template = "nest/blocks/call_to_action_link.html"
        label = _("Call to action link")
        icon = "link"
        max_num = 1
        help_text = _(
            "A call to action link to a page of this website " "or to a specific URL"
        )

    label = LabelBlock(required=False)
    link = LinkStreamBlock(required=True)
