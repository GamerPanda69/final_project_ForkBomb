# banking/models.py
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from decimal import Decimal # Import Decimal for precision

class Account(models.Model):
    # Use OneToOneField for a strict one-account-per-user relationship
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='account')
    # Use DecimalField for monetary values to avoid floating-point issues
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))

    def __str__(self):
        return f"{self.user.username}'s Account (Balance: ₹{self.balance:.2f})"

    def clean(self):
        # Add validation to prevent negative balances if desired
        if self.balance < Decimal('0.00'):
            # Depending on requirements, you might allow temporary negative balances (overdraft)
            # For simplicity here, we prevent it.
            # raise ValidationError("Balance cannot be negative.")
            pass # Allow negative for now, handle withdrawal logic in view

    def save(self, *args, **kwargs):
        self.full_clean() # Run validation before saving
        super().save(*args, **kwargs)

# You might add a Transaction model later to track history
# class Transaction(models.Model):
#     account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='transactions')
#     amount = models.DecimalField(max_digits=12, decimal_places=2)
#     transaction_type = models.CharField(max_length=10, choices=[('DEPOSIT', 'Deposit'), ('WITHDRAW', 'Withdraw')])
#     timestamp = models.DateTimeField(auto_now_add=True)
#     description = models.CharField(max_length=255, blank=True, null=True)
#
#     def __str__(self):
#         return f"{self.transaction_type} of ₹{self.amount} for {self.account.user.username}"