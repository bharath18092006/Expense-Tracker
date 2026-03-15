from django.db.models import QuerySet

from .models import Expense


class ExpenseService:
    @staticmethod
    def filtered_queryset(user, params) -> QuerySet:
        queryset = Expense.objects.filter(owner=user)
        start_date = params.get("start_date")
        end_date = params.get("end_date")
        category = params.get("category")
        min_amount = params.get("min_amount")
        max_amount = params.get("max_amount")
        search = params.get("q")
        ordering = params.get("ordering", "-date")

        if start_date:
            queryset = queryset.filter(date__gte=start_date)
        if end_date:
            queryset = queryset.filter(date__lte=end_date)
        if category:
            queryset = queryset.filter(category__icontains=category)
        if min_amount:
            queryset = queryset.filter(amount__gte=min_amount)
        if max_amount:
            queryset = queryset.filter(amount__lte=max_amount)
        if search:
            queryset = queryset.filter(description__icontains=search)
        if ordering.lstrip("-") in {"date", "amount", "category"}:
            queryset = queryset.order_by(ordering)
        else:
            queryset = queryset.order_by("-date")
        return queryset

    @staticmethod
    def create_expense(user, validated_data):
        return Expense.objects.create(owner=user, **validated_data)
