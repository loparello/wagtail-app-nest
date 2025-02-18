from datetime import datetime, timedelta

from django.core.paginator import (
    Page,
    EmptyPage,
    PageNotAnInteger,
    Paginator,
)
from django.core.mail import EmailMultiAlternatives
from django.utils import timezone
from django.utils.text import slugify
from django.template.loader import render_to_string
from django.apps import apps
from django.conf import settings

from wagtail.models import Site
from wagtail.images import get_image_model


class SeoItem:
    """
    To use in views or other contexts where a page or a model object is not
    available to provide fields for the meta tags
    """

    def __init__(self, title="", description="", image=None, url_query=""):
        self.seo_title = title
        self.search_description = description
        if image:
            self.image = self.get_image(image)
        self.url_query = url_query

    def get_image(self, image):
        Image = get_image_model()
        try:
            # Checks if image is a Wagtail Image
            Image.objects.get(pk=image.id)
            return image
        except Image.DoesNotExist:
            raise Image.DoesNotExist("'SeoItem' image is not a Wagtail Image instance")


def get_unique_slug(obj, slugable_field_name, slug_field_name, limits={}) -> str:
    """
    Takes a model object, sluggable field name (such as 'title') of that
    model as string, slug field name (such as 'slug') of the model as string;
    returns a unique slug as string. Additional filters can be passed as dictionary
    to limit the range of uniqueness.
    """
    filters = {**limits}
    unique_slug = slugify(getattr(obj, slugable_field_name))
    filters[slug_field_name] = unique_slug

    extension = 1
    ModelClass = obj.__class__

    while ModelClass.objects.filter(**filters).exists():
        unique_slug = "{}-{}".format(unique_slug, extension)
        filters[slug_field_name] = unique_slug
        extension += 1

    return unique_slug


def paginate(request, items, offset, page_param="page") -> Page:
    """
    Paginates a query set and by getting the "page" query param
    from the request object it returns the subset of paginated
    items for that page.
    """
    paginator = Paginator(items, offset)
    # Try to get the ?page=x value
    page = request.GET.get(page_param)

    try:
        # If the page exists and the ?page=x is an int
        return paginator.page(page)
    except PageNotAnInteger:
        # If the ?page=x is not an int; show the first page
        return paginator.page(1)
    except EmptyPage:
        # If the ?page=x is out of range (too high most likely)
        # Then return the last page
        return paginator.page(paginator.num_pages)


def get_orderable_live_pages(items, return_orderables=False) -> list:
    """
    To be used when accessing related pages from oderables/inline penels. It
    will return a list of live pages with all the specific fields.
    Pass "return_orderables=True" to return the orderable objects and not
    directly the nested page objects.
    """
    if return_orderables:
        return [x for x in items.all() if x.page.live]

    return [x.page.specific for x in items.all() if x.page.live]


def get_orderable_snippets(items, snippet_field) -> list:
    if snippet_field:
        return [x[snippet_field] for x in items.all()]

    return items.all()


def get_settings(site, model_name, app_name):
    """To retrieve a site setting model"""
    settings_model = apps.get_model(app_name, model_name)
    return settings_model.for_site(site)


def get_email_html_or_text(
    html_template,
    plaintext_template,
    title="",
    context=None,
    sender=settings.DEFAULT_FROM_EMAIL,
    recipients=None,
) -> EmailMultiAlternatives:
    if context is None:
        context = {}
    if recipients is None:
        recipients = []
    # Render email text
    email_html_message = render_to_string(html_template, context)
    email_plaintext_message = render_to_string(plaintext_template, context)

    # Create email object
    msg = EmailMultiAlternatives(
        title,
        email_plaintext_message,
        sender,
        recipients,
    )
    msg.attach_alternative(email_html_message, "text/html")
    return msg


def is_date_past_num_days(target_date, num_days=1) -> bool:
    if target_date and isinstance(target_date, datetime):
        limit_date = timezone.now() - timedelta(days=num_days)
        return target_date < limit_date
    else:
        return False


def get_default_site() -> Site:
    return Site.objects.filter(is_default_site=True).first()
