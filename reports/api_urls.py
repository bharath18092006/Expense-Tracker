from django.urls import path

from .api_views import ReportSnapshotApi


urlpatterns = [
    path("snapshot/", ReportSnapshotApi.as_view(), name="api-v2-report-snapshot"),
]
