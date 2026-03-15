from django.urls import include, path


urlpatterns = [
    path("accounts/", include("accounts.api_urls")),
    path("expenses/", include("expenses.api_urls")),
    path("income/", include("income.api_urls")),
    path("goals/", include("goals.api_urls")),
    path("analytics/", include("analytics.api_urls")),
    path("reports/", include("reports.api_urls")),
]
