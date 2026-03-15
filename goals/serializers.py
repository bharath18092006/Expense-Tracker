from django.utils import timezone
from rest_framework import serializers

from .models import Goal


class GoalSerializer(serializers.ModelSerializer):
    progress = serializers.SerializerMethodField()

    class Meta:
        model = Goal
        fields = (
            "id",
            "name",
            "start_date",
            "end_date",
            "amount_to_save",
            "current_saved_amount",
            "progress",
        )
        read_only_fields = ("id", "progress")

    def get_progress(self, obj):
        return obj.calculate_progress()

    def validate(self, attrs):
        start_date = attrs.get("start_date", getattr(self.instance, "start_date", None))
        end_date = attrs.get("end_date", getattr(self.instance, "end_date", None))
        amount_to_save = attrs.get("amount_to_save", getattr(self.instance, "amount_to_save", None))

        if start_date and end_date and end_date < start_date:
            raise serializers.ValidationError("end_date must be on or after start_date.")
        if amount_to_save is not None and amount_to_save <= 0:
            raise serializers.ValidationError("amount_to_save must be greater than zero.")
        if start_date and start_date > timezone.now().date():
            raise serializers.ValidationError("start_date cannot be in the future.")
        return attrs
