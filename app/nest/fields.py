from django.db import models
from django.utils.translation import gettext_lazy as _

from wagtail.fields import StreamField, RichTextField
from wagtail.images import get_image_model_string
from wagtail.documents import get_document_model_string

from nest.blocks import BodyTextBlock, BodyTextWithMediaBlock


def ForeignKeyField(
    model,
    required=False,
    on_delete=models.SET_NULL,
    related_name="+",
    help_text="",
    **kargs,
) -> models.ForeignKey:
    """Wrapper function around the ForeignKey class"""
    blank = not required

    return models.ForeignKey(
        model,
        null=True,
        blank=blank,
        on_delete=on_delete,
        related_name=related_name,
        help_text=help_text,
        **kargs,
    )


def WagtailPageField(required=False, help_text="", **kargs) -> models.ForeignKey:
    """Wrapper function around the ForeignKey class specific for Wagtail pages"""
    return ForeignKeyField(
        "wagtailcore.Page",
        required=required,
        help_text=help_text,
        **kargs,
    )


def WagtailImageField(required=False, help_text="", **kargs) -> models.ForeignKey:
    """Wrapper function around the ForeignKey class specific for Wagtail images"""
    return ForeignKeyField(
        get_image_model_string(),
        required=required,
        help_text=help_text,
        **kargs,
    )


def WagtailDocumentField(required=False, help_text="", **kargs) -> models.ForeignKey:
    """Wrapper function around the ForeignKey class specific for Wagtail documents"""
    return ForeignKeyField(
        get_document_model_string(),
        required=required,
        help_text=help_text,
        **kargs,
    )


def ChoiceField(
    choices, required=False, is_numeric=False, default=None, help_text="", **kwargs
) -> models.Field:
    """
    Wrapper function around the Charfield or PositiveSmallIntegerField
    based on the is_numeric flag.
    The Charfield is used for the non-numeric choices.
    The PositiveSmallIntegerField is used for the numeric choices.
    """
    blank = not required
    default_choice = (
        default if default else choices[0][0] if required else 0 if is_numeric else ""
    )

    if is_numeric:
        return models.PositiveSmallIntegerField(
            blank=blank,
            default=default_choice,
            choices=choices,
            help_text=help_text,
            **kwargs,
        )

    return models.CharField(
        blank=blank,
        default=default_choice,
        max_length=50,
        choices=choices,
        help_text=help_text,
        **kwargs,
    )


def TitleField(
    required=False, verbose_name=_("title"), default="", help_text="", **kargs
) -> models.CharField:
    blank = not required

    return models.CharField(
        blank=blank,
        verbose_name=verbose_name,
        max_length=255,
        default=default,
        help_text=help_text,
        **kargs,
    )


def DescriptionField(
    required=False,
    richtext=False,
    features=["bold", "italic", "link", "ol", "ul"],
    verbose_name=_("description"),
    help_text="",
    **kargs,
) -> models.Field:
    blank = not required

    if richtext:
        return RichTextField(
            blank=blank,
            verbose_name=verbose_name,
            features=features,
            help_text=help_text,
            **kargs,
        )

    return models.TextField(
        blank=blank,
        verbose_name=verbose_name,
        help_text=help_text,
        **kargs,
    )


def LabelField(
    required=False, verbose_name=_("label"), default="Read more", help_text="", **kargs
) -> models.CharField:
    blank = not required

    return models.CharField(
        blank=blank,
        verbose_name=verbose_name,
        max_length=100,
        default=default,
        help_text=help_text,
        **kargs,
    )


def ExcerptField(
    required=False,
    verbose_name=_("excerpt"),
    help_text=_(
        "Optional. A short summary of the content to be used in "
        "previews and links. Optimal length is 200 characters"
    ),
    **kargs,
) -> models.TextField:
    blank = not required

    return models.TextField(
        blank=blank,
        verbose_name=verbose_name,
        help_text=help_text,
        **kargs,
    )


def PageHeroImageField(required=False) -> models.ForeignKey:
    """Extended version of WagtailImageField for page hero images. Allows some
    pages to have mandatory hero images.
    """
    return WagtailImageField(
        verbose_name=_("image"),
        required=required,
        help_text=_(
            ("Required. " if required else "Optional. ")
            + "The main image representing the page. "
            "It will be used as cover and in links and previews "
            "both internal and external, like social media or search "
            "engines. Optimal recommended image size is 2400x1600px"
        ),
    )


def BodyTextStreamField(
    required=False,
    verbose_name=_("Body text"),
    default="",
    **kargs,
) -> StreamField:
    """Function for body text stream field"""
    blank = not required

    return StreamField(
        BodyTextBlock(),
        verbose_name=verbose_name,
        blank=blank,
        default=default,
        use_json_field=True,
        **kargs,
    )


def BodyTextWithMediaStreamField(
    required=False,
    verbose_name=_("Body text"),
    default="",
    **kargs,
) -> StreamField:
    """Function for body text stream field with image and video blocks"""
    blank = not required

    return StreamField(
        BodyTextWithMediaBlock(),
        verbose_name=verbose_name,
        blank=blank,
        default=default,
        use_json_field=True,
        **kargs,
    )
