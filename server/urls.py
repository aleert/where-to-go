
"""
Main URL mapping configuration file.

Include other URLConfs from external apps using method `include()`.

It is also a good practice to keep a single URL to the root index page.

This examples uses Django's default media
files serving technique in development.
"""

from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView

from server.apps.places.views import home

urlpatterns = [
    path('', home, name='home'),
    path(
        'about/', TemplateView.as_view(template_name='pages/about.html'), name='about',
    ),
    path(settings.ADMIN_URL, admin.site.urls),

    # users management
    path('users/', include('server.apps.users.urls', namespace='users')),
    path('accounts/', include('allauth.urls')),  # noqa: DJ05
    # we don't have an api, but since we have one view and it serves json for frontend
    # let's call it so
    path('api/v1/', include('server.apps.places.urls', namespace='places')),
]

if settings.DEBUG:  # pragma: no cover
    import debug_toolbar  # noqa: WPS433
    from django.conf.urls.static import static  # noqa: WPS433

    urlpatterns = [
        # URLs specific only to django-debug-toolbar:
        path('__debug__/', include(debug_toolbar.urls)),  # noqa: DJ05
    ] + urlpatterns + static(
        # Serving media files in development only:
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )
