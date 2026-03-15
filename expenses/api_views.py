from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import Category, Expense
from .serializers import CategorySerializer, ExpenseSerializer
from .services import ExpenseService


class ExpenseListCreateApi(generics.ListCreateAPIView):
    serializer_class = ExpenseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ExpenseService.filtered_queryset(self.request.user, self.request.query_params)

    def perform_create(self, serializer):
        serializer.instance = ExpenseService.create_expense(self.request.user, serializer.validated_data)


class ExpenseDetailApi(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ExpenseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Expense.objects.filter(owner=self.request.user)


class CategoryListApi(generics.ListAPIView):
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]
    queryset = Category.objects.all().order_by("name")
