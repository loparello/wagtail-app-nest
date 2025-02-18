from django.urls import path
from django.shortcuts import get_object_or_404

from wagtail.api.v2.views import PagesAPIViewSet
from wagtail.api.v2.router import WagtailAPIRouter
from wagtail.images.api.v2.views import ImagesAPIViewSet
from wagtail.documents.api.v2.views import DocumentsAPIViewSet

from rest_framework.response import Response


api_router = WagtailAPIRouter("wagtailapi")


class ExtendedPagesAPIViewSet(PagesAPIViewSet):
    """
    Extends the default page view set so that the slug field
    can be used as main detail lookup as well, with path "/pages/slug/<page_slug>"
    """

    lookup_fields = ["pk", "slug"]

    def get_object(self):
        queryset = self.get_queryset()
        queryset = self.filter_queryset(queryset)

        filter_kwargs = {}
        for field in self.lookup_fields:
            if self.kwargs.get(field, None):
                filter_kwargs[field] = self.kwargs[field]

        obj = get_object_or_404(queryset, **filter_kwargs)  # Lookup the object
        self.check_object_permissions(self.request, obj)
        return obj.specific  # Get specific page fields (Only works with pages)

    def detail_view(self, request, pk=None, slug=None):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @classmethod
    def get_urlpatterns(cls):
        """
        This returns a list of URL patterns for the endpoint
        """
        return [
            path("", cls.as_view({"get": "listing_view"}), name="listing"),
            path("<int:pk>/", cls.as_view({"get": "detail_view"}), name="detail"),
            path(
                "slug/<str:slug>/",
                cls.as_view({"get": "detail_view"}),
                name="detail_by_slug",
            ),
            path("find/", cls.as_view({"get": "find_view"}), name="find"),
        ]


api_router.register_endpoint("pages", ExtendedPagesAPIViewSet)
api_router.register_endpoint("images", ImagesAPIViewSet)
api_router.register_endpoint("documents", DocumentsAPIViewSet)
