from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .finance_tools import *

@login_required
def tools(request):
    result = None
    error = None
    if request.method == 'POST':
        tool = request.POST.get('tool')
        try:
            if tool == 'emi':
                principal = float(request.POST['principal'])
                rate = float(request.POST['rate'])
                tenure = int(request.POST['tenure'])
                result = f"EMI: ₹{calculate_emi(principal, rate, tenure)}"
            elif tool == 'sip':
                investment = float(request.POST['investment'])
                rate = float(request.POST['rate'])
                tenure = int(request.POST['tenure'])
                result = f"SIP Maturity: ₹{calculate_sip(investment, rate, tenure)}"
            elif tool == 'fd':
                principal = float(request.POST['principal'])
                rate = float(request.POST['rate'])
                tenure = int(request.POST['tenure'])
                result = f"FD Maturity: ₹{calculate_fd(principal, rate, tenure)}"
            elif tool == 'rd':
                deposit = float(request.POST['deposit'])
                rate = float(request.POST['rate'])
                tenure = int(request.POST['tenure'])
                result = f"RD Maturity: ₹{calculate_rd(deposit, rate, tenure)}"
            elif tool == 'retirement':
                current_age = int(request.POST['current_age'])
                retirement_age = int(request.POST['retirement_age'])
                monthly_expenses = float(request.POST['monthly_expenses'])
                inflation_rate = float(request.POST['inflation_rate'])
                return_rate = float(request.POST['return_rate'])
                result = f"Retirement Corpus Needed: ₹{estimate_retirement_corpus(current_age, retirement_age, monthly_expenses, inflation_rate, return_rate)}"
            elif tool == 'home_loan':
                income = float(request.POST['income'])
                obligations = float(request.POST['obligations'])
                rate = float(request.POST['rate'])
                tenure = int(request.POST['tenure'])
                result = f"Max Loan Eligibility: ₹{estimate_home_loan_eligibility(income, obligations, rate, tenure)}"
            elif tool == 'credit_card':
                balance = float(request.POST['balance'])
                rate = float(request.POST['rate'])
                min_payment = float(request.POST['min_payment'])
                months = int(request.POST['months'])
                result = f"Remaining Balance: ₹{calculate_credit_card_balance(balance, rate, min_payment, months)}"
            elif tool == 'taxable_income':
                gross_income = float(request.POST['gross_income'])
                deductions = float(request.POST['deductions'])
                result = f"Taxable Income: ₹{calculate_taxable_income(gross_income, deductions)}"
            elif tool == 'budget':
                income = float(request.POST['income'])
                expenses = float(request.POST['expenses'])
                result = plan_budget(income, expenses)
            elif tool == 'net_worth':
                assets = float(request.POST['assets'])
                liabilities = float(request.POST['liabilities'])
                result = f"Net Worth: ₹{calculate_net_worth(assets, liabilities)}"
        except ValueError as e:
            error = str(e)
    return render(request, 'tools.html', {'result': result, 'error': error})