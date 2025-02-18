from django.db import models

from wagtail.images.models import Image, AbstractImage, AbstractRendition
from wagtail.documents.models import Document, AbstractDocument


class CustomImage(AbstractImage):
    # Add any extra fields to image here

    admin_form_fields = Image.admin_form_fields + (
        # Then add the field names here to make them appear in the form
    )


class CustomRendition(AbstractRendition):
    image = models.ForeignKey(
        CustomImage, on_delete=models.CASCADE, related_name="renditions"
    )

    class Meta:
        unique_together = (("image", "filter_spec", "focal_point_key"),)


class CustomDocument(AbstractDocument):
    # Add any extra fields to image here

    admin_form_fields = Document.admin_form_fields + (
        # Add all custom fields names to make them appear in the form
    )
