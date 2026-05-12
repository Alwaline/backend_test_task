from django.views.generic import RedirectView
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from api import urls as api_urls

urlpatterns = [
    path("api/v1/", include(api_urls)),
    path("api/v1/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/v1/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("", RedirectView.as_view(url="/api/v1/docs/", permanent=False)),
]
