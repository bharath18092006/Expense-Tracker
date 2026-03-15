from django.utils import timezone
from rest_framework import serializers

from userincome.models import UserIncome


class IncomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserIncome
        fields = ("id", "amount", "date", "description", "source")
        read_only_fields = ("id",)

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Amount must be greater than zero.")
        return value

    def validate_date(self, value):
        if value > timezone.now().date():
            raise serializers.ValidationError("Date cannot be in the future.")
        return value
