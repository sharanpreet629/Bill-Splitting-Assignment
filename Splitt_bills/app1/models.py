
from django.db import models

class User(models.Model):
    user_id = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    mobile = models.CharField(max_length=15)

    def __str__(self):
        return self.name

class Expense(models.Model):
    EXPENSE_TYPE_CHOICES = [
        ('EQUAL', 'Equal'),
        ('EXACT', 'Exact'),
        ('PERCENT', 'Percent'),
    ]

    payer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='expenses_paid')
    participants = models.ManyToManyField(User, related_name='expenses_participated')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    expense_type = models.CharField(max_length=10, choices=EXPENSE_TYPE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.payer.name} paid {self.amount} ({self.expense_type})"

class Balance(models.Model):
    creditor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='creditor_balances')
    debtor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='debtor_balances')
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.debtor.name} owes {self.creditor.name} {self.amount}"


