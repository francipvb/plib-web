from typing import Type

from django.urls import path
from drf_spectacular.extensions import OpenApiViewExtension
from drf_spectacular.utils import (
    OpenApiExample,
    OpenApiResponse,
    PolymorphicProxySerializer,
    extend_schema,
    extend_schema_serializer,
)
from drf_spectacular.views import (
    SpectacularJSONAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
    SpectacularYAMLAPIView,
)
from rest_auth.serializers import (
    JWTSerializer,
    LoginSerializer,
    TokenSerializer,
    UserDetailsSerializer,
)
from rest_auth.views import LoginView, LogoutView, UserDetailsView
from rest_framework.views import APIView


@extend_schema_serializer(
    examples=[
        OpenApiExample("username", "example"),
        OpenApiExample("email", "email@example.com"),
        OpenApiExample("first_name", "John"),
        OpenApiExample("last_name", "Doe"),
    ]
)
class UserSerializer(UserDetailsSerializer):
    pass


class JWTTokenSerializer(JWTSerializer):
    user = UserSerializer()


@extend_schema_serializer(
    examples=[
        OpenApiExample("username", {"username": "johndoe", "password": "C0mplexPassw0rd"}),
        OpenApiExample("email", {"email": "johndoe@example.com", "password": "C0mplexPassw0rd"}),
    ]
)
class LoginSerializer(LoginSerializer):
    pass


class LoginViewFixer(OpenApiViewExtension):
    target_class = "rest_auth.views.LoginView"

    def view_replacement(self) -> Type[APIView]:
        @extend_schema(
            responses=PolymorphicProxySerializer(
                component_name="LoginResponse",
                serializers={
                    "key": TokenSerializer,
                    "token": JWTTokenSerializer,
                },
                resource_type_field_name="LoginResponse",
            ),
            request=LoginSerializer,
        )
        class ReplacedLoginView(LoginView):
            pass

        return ReplacedLoginView


class LogoutViewFixer(OpenApiViewExtension):
    target_class = "rest_auth.views.LogoutView"

    def view_replacement(self) -> "Type[APIView]":
        @extend_schema(
            responses=OpenApiResponse(None, "Returns nothing."),
            request=None,
        )
        class ReplacedLogoutView(LogoutView):
            pass

        return ReplacedLogoutView
        return super().view_replacement()


class UserViewFixer(OpenApiViewExtension):
    target_class = "rest_auth.views.UserDetailsView"

    def view_replacement(self) -> "Type[APIView]":
        @extend_schema(request=UserSerializer, responses=UserSerializer)
        class ReplacedUserDetailsView(UserDetailsView):
            pass

        return ReplacedUserDetailsView


urlpatterns = [
    path("schema.json", SpectacularJSONAPIView.as_view(), name="json-schema"),
    path("schema.yaml", SpectacularYAMLAPIView.as_view()),
    path("swagger.html", SpectacularSwaggerView.as_view(url_name="json-schema")),
    path("redoc.html", SpectacularRedocView.as_view(url_name="json-schema")),
]
