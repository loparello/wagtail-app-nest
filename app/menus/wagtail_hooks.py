from wagtail.snippets.models import register_snippet

from .views import MenuViewSet


register_snippet(MenuViewSet)
