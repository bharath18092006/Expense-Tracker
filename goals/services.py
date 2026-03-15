from django.db import models

from .models import Goal


class GoalService:
    @staticmethod
    def filtered_queryset(user, params):
        queryset = Goal.objects.filter(owner=user)
        status_filter = params.get("status")
        if status_filter == "active":
            queryset = queryset.filter(current_saved_amount__lt=models.F("amount_to_save"))
        elif status_filter == "completed":
            queryset = queryset.filter(current_saved_amount__gte=models.F("amount_to_save"))
        return queryset.order_by("end_date")

    @staticmethod
    def create_goal(user, validated_data):
        return Goal.objects.create(owner=user, **validated_data)
