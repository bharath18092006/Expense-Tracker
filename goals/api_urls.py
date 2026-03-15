from django.urls import path

from .api_views import GoalDetailApi, GoalListCreateApi


urlpatterns = [
    path("", GoalListCreateApi.as_view(), name="api-v2-goal-list"),
    path("<int:pk>/", GoalDetailApi.as_view(), name="api-v2-goal-detail"),
]
