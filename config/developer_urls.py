from django.urls import path
from drf_spectacular.views import (
    SpectacularJSONAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
    SpectacularYAMLAPIView,
)

urlpatterns = [
    path("schema.json", SpectacularJSONAPIView.as_view(), name="json-schema"),
    path("schema.yaml", SpectacularYAMLAPIView.as_view()),
    path("swagger.html", SpectacularSwaggerView.as_view(url_name="json-schema")),
    path("redoc.html", SpectacularRedocView.as_view(url_name="json-schema")),
]
