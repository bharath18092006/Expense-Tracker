from django.urls import path

from .api_views import (
    CategorySpendingApi,
    DashboardSnapshotApi,
    ForecastPredictionApi,
    IncomeVsExpenseApi,
    MonthlyExpenseSummaryApi,
)


urlpatterns = [
    path("dashboard/", DashboardSnapshotApi.as_view(), name="api-v2-dashboard"),
    path("monthly-expense-summary/", MonthlyExpenseSummaryApi.as_view(), name="api-v2-monthly-expense"),
    path("income-vs-expense/", IncomeVsExpenseApi.as_view(), name="api-v2-income-vs-expense"),
    path("category-spending/", CategorySpendingApi.as_view(), name="api-v2-category-spending"),
    path("forecast-prediction/", ForecastPredictionApi.as_view(), name="api-v2-forecast"),
]
