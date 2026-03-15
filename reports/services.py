from django.db.models import Sum

from expenses.models import Expense
from userincome.models import UserIncome


class ReportService:
    @staticmethod
    def period_snapshot(user, start_date, end_date):
        expenses = Expense.objects.filter(owner=user, date__range=[start_date, end_date])
        income = UserIncome.objects.filter(owner=user, date__range=[start_date, end_date])
        total_expense = expenses.aggregate(total=Sum("amount"))["total"] or 0
        total_income = income.aggregate(total=Sum("amount"))["total"] or 0
        return {
            "start_date": start_date,
            "end_date": end_date,
            "total_income": float(total_income),
            "total_expense": float(total_expense),
            "savings": float(total_income - total_expense),
        }
