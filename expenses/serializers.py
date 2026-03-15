from django.utils import timezone
from rest_framework import serializers

from .models import Category, Expense


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("id", "name")
        read_only_fields = ("id",)


class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = ("id", "amount", "date", "description", "category")
        read_only_fields = ("id",)

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Amount must be greater than zero.")
        return value

    def validate_date(self, value):
        if value > timezone.now().date():
            raise serializers.ValidationError("Date cannot be in the future.")
        return value
