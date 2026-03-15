from django.urls import path

from .api_views import MeApi


urlpatterns = [
    path("me/", MeApi.as_view(), name="api-v2-me"),
]
