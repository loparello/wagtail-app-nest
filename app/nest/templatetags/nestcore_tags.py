from django.template import Library, TemplateSyntaxError
from django.template.defaultfilters import stringfilter
from django.conf import settings

from wagtail.models import Site


register = Library()


@register.filter
def tostr(value) -> str:
    """Converts to string"""
    return str(value)


@register.filter
@stringfilter
def upto(value, delimiter=",") -> str:
    """Clears string of part after delimiter character"""
    return value.split(delimiter)[0]


@register.simple_tag
def updateurlparams(request, **kwargs) -> str:
    """Updates or adds url parameters by passing field=value pairs"""
    params_dict = request.GET.copy()

    for field, value in kwargs.items():
        params_dict[field] = value

    # Removes empty parameters to keep things neat
    for field in [field for field, value in params_dict.items() if not value]:
        del params_dict[field]

    return params_dict.urlencode()


@register.simple_tag
def appversion(with_site_name: bool = False) -> str:
    if with_site_name:
        return "{} v{}".format(settings.WAGTAIL_SITE_NAME, settings.VERSION)

    return "v{}".format(settings.VERSION)


@register.inclusion_tag("nest/partials/_meta_tags.html")
def meta_tags(request, item, is_post=False, use_url_params=False):
    """Renders page meta tags"""

    if not request:
        raise TemplateSyntaxError("'meta_tags' missing request")
    if not item:
        raise TemplateSyntaxError("'meta_tags' missing model object")

    site = Site.find_for_request(request)

    meta_image = None
    if getattr(item, "image", None):
        meta_image = item.image.get_rendition("fill-1200x630")

    context = {
        "request": request,
        "meta_title": getattr(item, "seo_title", "")
        or getattr(item, "title", "")
        or getattr(item, "name", ""),
        "meta_description": getattr(item, "search_description", "")
        or getattr(item, "excerpt", "")
        or getattr(item, "description", ""),
        "meta_image": meta_image,
        "site_name": site.site_name,
        "url": "{}{}".format(site.root_url, request.path),
        "opengraph_type": "website",
        "twitter_card_type": "summary",
    }

    if is_post:
        context["opengraph_type"] = "article"

    if context["meta_image"]:
        context["twitter_card_type"] = "summary_large_image"

    if use_url_params:
        context["url"] = "{}{}".format(site.root_url, request.get_full_path())

    url_query = getattr(item, "url_query", "")
    if url_query:
        context["url"] = "{}{}".format(context["url"], url_query)

    return context
