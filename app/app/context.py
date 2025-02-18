from django.conf import settings


def globals(request) -> dict:
    """Provides a global context to expose data in templates around the whole site"""
    # Add values here if needed in the admin templates as well
    globals = {
        "global": {
            "debug": settings.DEBUG,
        },
    }

    if request.path.startswith("/admin/") or request.path.startswith("/django-admin/"):
        if not request.path.endswith("/preview/"):
            return globals

    # Add values here if needed in the frontend templates only
    # e.g. globals["global"]["site"] = Site.find_for_request(request)

    return globals
