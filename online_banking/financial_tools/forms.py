# financial_tools/forms.py
from django import forms
from decimal import Decimal

# Define forms for each tool for better validation and structure
class EmiForm(forms.Form):
    principal = forms.DecimalField(min_value=Decimal('0.01'), label="Principal Amount (₹)")
    rate = forms.FloatField(min_value=0.01, label="Annual Interest Rate (%)")
    tenure = forms.IntegerField(min_value=1, label="Tenure (Years)")

class SipForm(forms.Form):
    investment = forms.DecimalField(min_value=Decimal('0.01'), label="Monthly Investment (₹)")
    rate = forms.FloatField(min_value=0.01, label="Annual Return Rate (%)")
    tenure = forms.IntegerField(min_value=1, label="Tenure (Years)")

class FdForm(forms.Form):
    principal = forms.DecimalField(min_value=Decimal('0.01'), label="Principal Amount (₹)")
    rate = forms.FloatField(min_value=0.01, label="Annual Interest Rate (%)")
    tenure = forms.FloatField(min_value=0.1, label="Tenure (Years)") # Allow fractional years for FD

class RdForm(forms.Form):
    deposit = forms.DecimalField(min_value=Decimal('0.01'), label="Monthly Deposit (₹)")
    rate = forms.FloatField(min_value=0.01, label="Annual Interest Rate (%)")
    tenure = forms.IntegerField(min_value=1, label="Tenure (Years)")

class RetirementForm(forms.Form):
    current_age = forms.IntegerField(min_value=1, label="Current Age")
    retirement_age = forms.IntegerField(min_value=1, label="Target Retirement Age")
    monthly_expenses = forms.DecimalField(min_value=Decimal('0.01'), label="Current Monthly Expenses (₹)")
    inflation_rate = forms.FloatField(min_value=0, label="Expected Annual Inflation Rate (%)")
    return_rate = forms.FloatField(min_value=0, label="Expected Post-Retirement Annual Return Rate (%)")

    def clean(self):
        cleaned_data = super().clean()
        current_age = cleaned_data.get("current_age")
        retirement_age = cleaned_data.get("retirement_age")
        if current_age and retirement_age and current_age >= retirement_age:
            raise forms.ValidationError("Retirement age must be greater than current age.")
        return cleaned_data

class HomeLoanEligibilityForm(forms.Form):
    income = forms.DecimalField(min_value=Decimal('0.01'), label="Monthly Income (₹)")
    obligations = forms.DecimalField(min_value=Decimal('0.00'), label="Total Monthly Obligations (Other EMIs, etc.) (₹)")
    rate = forms.FloatField(min_value=0.01, label="Annual Interest Rate (%)")
    tenure = forms.IntegerField(min_value=1, label="Loan Tenure (Years)")

class CreditCardForm(forms.Form):
    balance = forms.DecimalField(min_value=Decimal('0.01'), label="Current Card Balance (₹)")
    rate = forms.FloatField(min_value=0.01, label="Annual Interest Rate (%)")
    min_payment = forms.FloatField(min_value=0.01, label="Minimum Payment (%)")
    months = forms.IntegerField(min_value=1, label="Number of Months")

class TaxableIncomeForm(forms.Form):
    gross_income = forms.DecimalField(min_value=Decimal('0.00'), label="Gross Annual Income (₹)")
    deductions = forms.DecimalField(min_value=Decimal('0.00'), label="Total Deductions (₹)")

class BudgetForm(forms.Form):
    income = forms.DecimalField(min_value=Decimal('0.00'), label="Monthly Income (₹)")
    expenses = forms.DecimalField(min_value=Decimal('0.00'), label="Total Monthly Expenses (₹)")

class NetWorthForm(forms.Form):
    assets = forms.DecimalField(min_value=Decimal('0.00'), label="Total Assets (₹)")
    liabilities = forms.DecimalField(min_value=Decimal('0.00'), label="Total Liabilities (₹)")

# Dictionary to map tool names to forms
TOOL_FORMS = {
    'emi': EmiForm,
    'sip': SipForm,
    'fd': FdForm,
    'rd': RdForm,
    'retirement': RetirementForm,
    'home_loan': HomeLoanEligibilityForm,
    'credit_card': CreditCardForm,
    'taxable_income': TaxableIncomeForm,
    'budget': BudgetForm,
    'net_worth': NetWorthForm,
}

# Dictionary for user-friendly display names (add this)
TOOL_NAMES = {
    'emi': 'EMI',
    'sip': 'SIP',
    'fd': 'Fixed Deposit (FD)',
    'rd': 'Recurring Deposit (RD)',
    'retirement': 'Retirement Corpus',
    'home_loan': 'Home Loan Eligibility',
    'credit_card': 'Credit Card Payoff',
    'taxable_income': 'Taxable Income',
    'budget': 'Budget Planner',
    'net_worth': 'Net Worth',
}