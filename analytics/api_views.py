from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .services import DashboardAnalyticsService


class RangeQuerySerializer(serializers.Serializer):
    start_date = serializers.DateField(required=False)
    end_date = serializers.DateField(required=False)
    months = serializers.IntegerField(required=False, min_value=1, max_value=24)
    days = serializers.IntegerField(required=False, min_value=1, max_value=365)

    def validate(self, attrs):
        start_date = attrs.get("start_date")
        end_date = attrs.get("end_date")
        if start_date and end_date and start_date > end_date:
            raise serializers.ValidationError("start_date must be before end_date.")
        return attrs


class DashboardSnapshotApi(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(DashboardAnalyticsService.dashboard_snapshot(request.user))


class MonthlyExpenseSummaryApi(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = RangeQuerySerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        months = serializer.validated_data.get("months", 6)
        data = DashboardAnalyticsService.monthly_expense_summary(request.user, months=months)
        return Response({"results": data})


class IncomeVsExpenseApi(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = RangeQuerySerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        months = serializer.validated_data.get("months", 6)
        data = DashboardAnalyticsService.income_vs_expense_summary(request.user, months=months)
        return Response({"results": data})


class CategorySpendingApi(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = RangeQuerySerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        data = DashboardAnalyticsService.category_spending(
            request.user,
            start_date=serializer.validated_data.get("start_date"),
            end_date=serializer.validated_data.get("end_date"),
        )
        return Response({"results": data})


class ForecastPredictionApi(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = RangeQuerySerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        days = serializer.validated_data.get("days", 30)
        data = DashboardAnalyticsService.quick_forecast(request.user, days=days)
        return Response(data)
