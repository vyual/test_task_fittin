"""
URL configuration for test_task project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import debug_toolbar
from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache

from django.conf.urls.static import static


@login_required
def custom_swagger_view(request, *args, **kwargs):
    return SpectacularSwaggerView.as_view(url_name="schema")(request, *args, **kwargs)


@login_required
def custom_redoc_view(request, *args, **kwargs):
    return SpectacularRedocView.as_view(url_name="schema")(request, *args, **kwargs)


@login_required
def custom_schema_view(request, *args, **kwargs):
    return SpectacularAPIView.as_view()(request, *args, **kwargs)


urlpatterns = (
    [
    path("admin/", admin.site.urls),
    path("account/", include("account.urls")),
    path("api/shop/", include("shop.urls")),
    path("api/schema/", never_cache(custom_schema_view), name="schema"),
    path("api/swagger/", never_cache(custom_swagger_view), name="swagger-ui"),
    path("api/redoc/", never_cache(custom_redoc_view), name="redoc"),

]   
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    )

if settings.DEBUG:
    urlpatterns += [
        path("__debug__/", include(debug_toolbar.urls)),
    ]
