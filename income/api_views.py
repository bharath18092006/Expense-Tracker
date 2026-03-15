from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from userincome.models import UserIncome

from .serializers import IncomeSerializer
from .services import IncomeService


class IncomeListCreateApi(generics.ListCreateAPIView):
    serializer_class = IncomeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return IncomeService.filtered_queryset(self.request.user, self.request.query_params)

    def perform_create(self, serializer):
        serializer.instance = IncomeService.create_income(self.request.user, serializer.validated_data)


class IncomeDetailApi(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = IncomeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return UserIncome.objects.filter(owner=self.request.user)
