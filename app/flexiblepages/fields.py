from django.utils.translation import gettext_lazy as _

from wagtail.fields import StreamField

from nest.blocks import BodyTextWithMediaBlock
from flexiblepages.blocks import DetailBlock


def ContentStreamField(required=False, verbose_name=_("Content")) -> StreamField:
    blank = not required

    return StreamField(
        [
            ("body_text", BodyTextWithMediaBlock()),
            ("detail", DetailBlock()),
        ],
        verbose_name=verbose_name,
        blank=blank,
        use_json_field=True,
    )
