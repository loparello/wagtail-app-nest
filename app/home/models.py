from nest.abstracts import BasePage
from nest.mixins import PageIntroMixin, PageLinkMixin


class HomePage(BasePage, PageIntroMixin, PageLinkMixin):
    max_count = 1

    content_panels = (
        BasePage.content_panels + PageIntroMixin.panels + PageLinkMixin.panels
    )
