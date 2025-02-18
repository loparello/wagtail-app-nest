from django.conf import settings
from django.urls import include, path
from django.contrib import admin
from django.views.generic import TemplateView

from wagtail.admin import urls as wagtailadmin_urls
from wagtail import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls

# from wagtail.contrib.sitemaps.views import sitemap

from search import views as search_views

# from nest.views import RobotsView
from .api import api_router


urlpatterns = [
    path("admin/", include(wagtailadmin_urls)),
    path("db-admin/", admin.site.urls),
    path("documents/", include(wagtaildocs_urls)),
    path("search/", search_views.search, name="search"),
    path("api/v1/", api_router.urls),
    # path("sitemap.xml", sitemap), # Enable to generate sitemap.xml.
    # path("robots.txt", RobotsView.as_view()), # Enable to generate robots.txt.
]


if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    # URLs available in debug mode only
    testurlpatterns = [
        path("test/404/", TemplateView.as_view(template_name="404.html")),
        path("test/500/", TemplateView.as_view(template_name="500.html")),
    ]
    urlpatterns += testurlpatterns

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += [
    # For anything not caught by a more specific rule above, hand over to
    # Wagtail's page serving mechanism. This should be the last pattern in
    # the list:
    path("", include(wagtail_urls)),
    # Alternatively, if you want Wagtail pages to be served from a subpath
    # of your site, rather than the site root:
    #    path("pages/", include(wagtail_urls)),
]
