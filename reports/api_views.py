from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .services import ReportService


class ReportQuerySerializer(serializers.Serializer):
    start_date = serializers.DateField()
    end_date = serializers.DateField()

    def validate(self, attrs):
        if attrs["start_date"] > attrs["end_date"]:
            raise serializers.ValidationError("start_date must be before end_date.")
        return attrs


class ReportSnapshotApi(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = ReportQuerySerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        data = ReportService.period_snapshot(
            request.user,
            serializer.validated_data["start_date"],
            serializer.validated_data["end_date"],
        )
        return Response(data)
