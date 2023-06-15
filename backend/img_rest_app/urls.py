"""img_rest_app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include, re_path
import images.views as views
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.views.decorators.csrf import csrf_exempt
from djoser.views import TokenCreateView

schema_view = get_schema_view(
    openapi.Info(
        title="API",
        default_version="v2",
        description="Description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="kovalev.vxx@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path(
        "api/auth/token/", csrf_exempt(TokenCreateView.as_view()), name="token_create"
    ),
    path("admin/", admin.site.urls),
    path("api/photos/", views.PhotoListView.as_view()),
    path("api/colors/", views.ColorView.as_view()),
    path("api/keywords/", views.KeywordView.as_view()),
    path("api/user/", views.UserView.as_view()),
    path("api/search/", views.SearchPhotoListView.as_view()),
    path("api/user/likes/create", views.LikePhotoCreateView.as_view()),
    path("api/user/likes/<str:pk>", views.LikePhotoDetailView.as_view()),
    path("api/user/likes/", views.LikePhotoView.as_view()),
    path("api/user/collections/", views.CollectionExpandedView.as_view()),
    path("api/user/collections/create", views.CollectionCreateView.as_view()),
    path("api/user/collections/<int:pk>", views.CollectionDetailView.as_view()),
    path("api/auth/", include("djoser.urls")),
    re_path(r"^api/auth/", include("djoser.urls.authtoken")),
    path(
        "doc/swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path(
        "doc/redoc", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"
    ),
]
