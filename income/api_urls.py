from django.urls import path

from .api_views import IncomeDetailApi, IncomeListCreateApi


urlpatterns = [
    path("", IncomeListCreateApi.as_view(), name="api-v2-income-list"),
    path("<int:pk>/", IncomeDetailApi.as_view(), name="api-v2-income-detail"),
]
