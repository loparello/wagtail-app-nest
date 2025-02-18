from django.conf import settings
from django.utils.module_loading import import_string


def get_default_renderer_classes() -> list:
    renderer_classes = getattr(
        settings,
        "WAGTAILAPI_DEFAULT_RENDERER_CLASSES",
        [
            "rest_framework.renderers.JSONRenderer",
            "rest_framework.renderers.BrowsableAPIRenderer",
        ],
    )

    return [import_string(x) for x in renderer_classes]
