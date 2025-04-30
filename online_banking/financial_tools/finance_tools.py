def calculate_emi(principal, annual_interest_rate, tenure_years):
    """Calculate EMI for a loan."""
    if principal <= 0 or annual_interest_rate <= 0 or tenure_years <= 0:
        raise ValueError("Principal, interest rate, and tenure must be positive.")
    monthly_rate = annual_interest_rate / (12 * 100)
    months = tenure_years * 12
    emi = (principal * monthly_rate * (1 + monthly_rate) ** months) / ((1 + monthly_rate) ** months - 1)
    return round(emi, 2)

def calculate_sip(monthly_investment, annual_rate, tenure_years):
    """Calculate SIP maturity amount."""
    if monthly_investment <= 0 or annual_rate <= 0 or tenure_years <= 0:
        raise ValueError("Investment, rate, and tenure must be positive.")
    monthly_rate = annual_rate / (12 * 100)
    months = tenure_years * 12
    maturity = monthly_investment * (((1 + monthly_rate) ** months - 1) / monthly_rate) * (1 + monthly_rate)
    return round(maturity, 2)

def calculate_fd(principal, annual_rate, tenure_years):
    """Calculate Fixed Deposit maturity amount."""
    if principal <= 0 or annual_rate <= 0 or tenure_years <= 0:
        raise ValueError("Principal, rate, and tenure must be positive.")
    maturity = principal * (1 + annual_rate / 100) ** tenure_years
    return round(maturity, 2)

def calculate_rd(monthly_deposit, annual_rate, tenure_years):
    """Calculate Recurring Deposit maturity amount."""
    if monthly_deposit <= 0 or annual_rate <= 0 or tenure_years <= 0:
        raise ValueError("Deposit, rate, and tenure must be positive.")
    monthly_rate = annual_rate / (12 * 100)
    months = tenure_years * 12
    maturity = 0
    for i in range(1, months + 1):
        maturity += monthly_deposit * (1 + monthly_rate) ** (months - i + 1)
    return round(maturity, 2)

def estimate_retirement_corpus(current_age, retirement_age, monthly_expenses, inflation_rate, return_rate):
    """Estimate retirement corpus needed."""
    if current_age >= retirement_age or monthly_expenses <= 0 or inflation_rate < 0 or return_rate < 0:
        raise ValueError("Invalid input values.")
    years_to_retire = retirement_age - current_age
    future_expenses = monthly_expenses * (1 + inflation_rate / 100) ** years_to_retire
    corpus = future_expenses * 12 / (return_rate / 100)
    return round(corpus, 2)

def estimate_home_loan_eligibility(monthly_income, monthly_obligations, interest_rate, tenure_years):
    """Estimate maximum home loan eligibility."""
    if monthly_income <= 0 or monthly_obligations < 0 or interest_rate <= 0 or tenure_years <= 0:
        raise ValueError("Invalid input values.")
    disposable_income = monthly_income - monthly_obligations
    monthly_rate = interest_rate / (12 * 100)
    months = tenure_years * 12
    max_emi = disposable_income
    loan_amount = max_emi * (1 - (1 + monthly_rate) ** -months) / monthly_rate
    return round(loan_amount, 2)

def calculate_credit_card_balance(balance, annual_interest_rate, min_payment_percent, months):
    """Calculate credit card balance after minimum payments."""
    if balance <= 0 or annual_interest_rate <= 0 or min_payment_percent <= 0 or months < 0:
        raise ValueError("Invalid input values.")
    monthly_rate = annual_interest_rate / (12 * 100)
    for _ in range(months):
        interest = balance * monthly_rate
        min_payment = balance * (min_payment_percent / 100)
        balance = balance + interest - min_payment
        if balance <= 0:
            break
    return round(balance, 2)

def calculate_taxable_income(gross_income, deductions):
    """Calculate taxable income after deductions."""
    if gross_income < 0 or deductions < 0:
        raise ValueError("Income and deductions must be non-negative.")
    taxable_income = gross_income - deductions
    return max(0, round(taxable_income, 2))

def plan_budget(monthly_income, monthly_expenses):
    """Provide a simple budget plan."""
    if monthly_income < 0 or monthly_expenses < 0:
        raise ValueError("Income and expenses must be non-negative.")
    savings = monthly_income - monthly_expenses
    if savings > 0:
        return f"You can save ₹{savings:.2f} per month."
    elif savings < 0:
        return f"You are overspending by ₹{-savings:.2f} per month."
    else:
        return "Your budget is balanced."

def calculate_net_worth(assets, liabilities):
    """Calculate net worth."""
    if assets < 0 or liabilities < 0:
        raise ValueError("Assets and liabilities must be non-negative.")
    net_worth = assets - liabilities
    return round(net_worth, 2)