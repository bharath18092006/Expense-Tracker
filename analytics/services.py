from __future__ import annotations

from collections import defaultdict
from datetime import date, timedelta

from django.core.cache import cache
from django.db.models import Sum

from expenses.models import Expense
from goals.models import Goal
from userincome.models import UserIncome


class DashboardAnalyticsService:
    CACHE_TTL_SECONDS = 60 * 5

    @classmethod
    def _cache_key(cls, user_id: int, suffix: str) -> str:
        return f"dashboard:{user_id}:{suffix}"

    @classmethod
    def monthly_expense_summary(cls, user, months: int = 6):
        key = cls._cache_key(user.id, f"monthly_expenses:{months}")
        cached = cache.get(key)
        if cached is not None:
            return cached

        today = date.today()
        start = today - timedelta(days=months * 31)
        expenses = (
            Expense.objects.filter(owner=user, date__gte=start, date__lte=today)
            .values("date", "amount")
            .order_by("date")
        )
        monthly = defaultdict(float)
        for item in expenses:
            month_key = item["date"].strftime("%Y-%m")
            monthly[month_key] += float(item["amount"])
        result = [{"month": month, "total": round(total, 2)} for month, total in sorted(monthly.items())]
        cache.set(key, result, cls.CACHE_TTL_SECONDS)
        return result

    @classmethod
    def income_vs_expense_summary(cls, user, months: int = 6):
        key = cls._cache_key(user.id, f"income_vs_expense:{months}")
        cached = cache.get(key)
        if cached is not None:
            return cached

        today = date.today()
        start = today - timedelta(days=months * 31)
        incomes = UserIncome.objects.filter(owner=user, date__gte=start, date__lte=today).values("date", "amount")
        expenses = Expense.objects.filter(owner=user, date__gte=start, date__lte=today).values("date", "amount")

        buckets = defaultdict(lambda: {"income": 0.0, "expense": 0.0})
        for item in incomes:
            month_key = item["date"].strftime("%Y-%m")
            buckets[month_key]["income"] += float(item["amount"])
        for item in expenses:
            month_key = item["date"].strftime("%Y-%m")
            buckets[month_key]["expense"] += float(item["amount"])

        result = [
            {
                "month": month,
                "income": round(values["income"], 2),
                "expense": round(values["expense"], 2),
            }
            for month, values in sorted(buckets.items())
        ]
        cache.set(key, result, cls.CACHE_TTL_SECONDS)
        return result

    @staticmethod
    def category_spending(user, start_date=None, end_date=None):
        queryset = Expense.objects.filter(owner=user)
        if start_date:
            queryset = queryset.filter(date__gte=start_date)
        if end_date:
            queryset = queryset.filter(date__lte=end_date)
        rows = queryset.values("category").annotate(total=Sum("amount")).order_by("-total")
        return [{"category": row["category"], "total": float(row["total"])} for row in rows]

    @staticmethod
    def quick_forecast(user, days: int = 30):
        expenses = list(Expense.objects.filter(owner=user).order_by("-date").values_list("amount", flat=True)[:30])
        if not expenses:
            return {"days": days, "daily_average": 0, "predicted_total": 0}
        recent_window = expenses[:7] if len(expenses) >= 7 else expenses
        daily_average = sum(float(item) for item in recent_window) / len(recent_window)
        return {
            "days": days,
            "daily_average": round(daily_average, 2),
            "predicted_total": round(daily_average * days, 2),
        }

    @staticmethod
    def dashboard_snapshot(user):
        total_income = UserIncome.objects.filter(owner=user).aggregate(total=Sum("amount"))["total"] or 0
        total_expenses = Expense.objects.filter(owner=user).aggregate(total=Sum("amount"))["total"] or 0
        savings = float(total_income) - float(total_expenses)
        recent_expenses = list(
            Expense.objects.filter(owner=user)
            .order_by("-date")[:8]
            .values("id", "amount", "category", "description", "date")
        )
        goals = Goal.objects.filter(owner=user).order_by("end_date")
        goal_data = []
        for goal in goals:
            progress = goal.calculate_progress()
            goal_data.append(
                {
                    "id": goal.id,
                    "name": goal.name,
                    "saved_percentage": float(progress["saved_percentage"]),
                    "current_saved_amount": float(goal.current_saved_amount),
                    "amount_to_save": float(goal.amount_to_save),
                }
            )

        return {
            "total_income": float(total_income),
            "total_expenses": float(total_expenses),
            "savings": round(savings, 2),
            "balance": round(savings, 2),
            "recent_expenses": recent_expenses,
            "goals": goal_data,
        }
