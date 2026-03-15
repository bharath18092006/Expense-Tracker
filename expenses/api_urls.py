from django.urls import path

from .api_views import CategoryListApi, ExpenseDetailApi, ExpenseListCreateApi


urlpatterns = [
    path("", ExpenseListCreateApi.as_view(), name="api-v2-expense-list"),
    path("<int:pk>/", ExpenseDetailApi.as_view(), name="api-v2-expense-detail"),
    path("categories/", CategoryListApi.as_view(), name="api-v2-category-list"),
]
