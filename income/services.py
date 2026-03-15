from datetime import date

from django.db.models import QuerySet

from userincome.models import UserIncome


class IncomeService:
    @staticmethod
    def filtered_queryset(user, params) -> QuerySet:
        queryset = UserIncome.objects.filter(owner=user)
        start_date = params.get("start_date")
        end_date = params.get("end_date")
        source = params.get("source")
        min_amount = params.get("min_amount")
        max_amount = params.get("max_amount")
        search = params.get("q")
        ordering = params.get("ordering", "-date")

        if start_date:
            queryset = queryset.filter(date__gte=start_date)
        if end_date:
            queryset = queryset.filter(date__lte=end_date)
        if source:
            queryset = queryset.filter(source__icontains=source)
        if min_amount:
            queryset = queryset.filter(amount__gte=min_amount)
        if max_amount:
            queryset = queryset.filter(amount__lte=max_amount)
        if search:
            queryset = queryset.filter(description__icontains=search)
        if ordering.lstrip("-") in {"date", "amount", "source"}:
            queryset = queryset.order_by(ordering)
        else:
            queryset = queryset.order_by("-date")

        return queryset

    @staticmethod
    def create_income(user, validated_data):
        return UserIncome.objects.create(owner=user, **validated_data)

    @staticmethod
    def monthly_total_for_year(user, year: int | None = None):
        year = year or date.today().year
        months = [0] * 12
        incomes = UserIncome.objects.filter(owner=user, date__year=year).values("date", "amount")
        for item in incomes:
            months[item["date"].month - 1] += float(item["amount"])
        return months
