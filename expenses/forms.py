from django import forms

from .models import Expense


class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ["amount", "category", "description", "date"]
        widgets = {
            "amount": forms.NumberInput(attrs={"class": "form-control form-control-sm"}),
            "description": forms.TextInput(attrs={"class": "form-control form-control-sm", "id": "descriptionField"}),
            "category": forms.TextInput(attrs={"class": "form-control form-control-sm", "id": "categoryField", "readonly": "readonly"}),
            "date": forms.DateInput(attrs={"type": "date", "class": "form-control form-control-sm"}),
        }
