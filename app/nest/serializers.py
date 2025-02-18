from rest_framework import serializers

from wagtail.images.fields import image_format_name_to_content_type


class PictureSourcesField(serializers.Field):
    """
    URLs for the <source> elements.
    """

    def __init__(self, *args, size_field="size", **kwargs):
        super().__init__(*args, **kwargs)
        self.size_field = size_field

    def to_representation(self, value):
        return [
            {
                "type": image_format_name_to_content_type(format),
                "url": value.get_rendition(
                    f"format-{format}|{self.context[self.size_field]}"
                ).url,
            }
            for format in ("avif", "webp")
        ]


class ImageSrcField(serializers.Field):
    """
    Base URL for the <img src=""> attribute.
    """

    def __init__(self, *args, size_field="size", **kwargs):
        super().__init__(*args, **kwargs)
        self.size_field = size_field

    def to_representation(self, value):
        return value.get_rendition(f"{self.context[self.size_field]}|jpegquality-60").url


class PictureSerializer(serializers.Serializer):
    """
    Serializer to provide the data for a <picture> element.
    """

    id = serializers.IntegerField()
    title = serializers.CharField()
    sources = PictureSourcesField(source="*")
    src = ImageSrcField(source="*")


class PictureWithThumbnailSerializer(PictureSerializer):
    thumbnail_sources = PictureSourcesField(source="*", size_field="thumbnail_size")
    thumbnail_src = ImageSrcField(source="*", size_field="thumbnail_size")
