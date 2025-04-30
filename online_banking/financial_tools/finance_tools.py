# financial_tools/finance_tools.py
from decimal import Decimal, ROUND_HALF_UP # Make sure Decimal and rounding are imported

# ... (keep all other imports and functions like calculate_emi, etc.) ...

def calculate_emi(principal, annual_interest_rate, tenure_years):
    # ... (ensure this function also uses Decimal correctly if not already) ...
    try:
        principal_amount = Decimal(principal)
        rate_decimal = Decimal(annual_interest_rate) / Decimal(100)
        num_months = int(tenure_years * 12)

        if rate_decimal == 0:
            if num_months == 0: return Decimal(0) # Avoid division by zero
            return (principal_amount / Decimal(num_months)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

        monthly_rate = rate_decimal / Decimal(12)
        one_plus_r_n = (Decimal(1) + monthly_rate) ** num_months
        emi = principal_amount * monthly_rate * one_plus_r_n / (one_plus_r_n - Decimal(1))
        return emi.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    except Exception as e:
        raise ValueError(f"Invalid input for EMI calculation: {e}")


def calculate_sip(monthly_investment, annual_return_rate, tenure_years):
    # ... (ensure this function also uses Decimal correctly if not already) ...
    try:
        investment = Decimal(monthly_investment)
        rate_decimal = Decimal(annual_return_rate) / Decimal(100)
        num_months = int(tenure_years * 12)

        if rate_decimal == 0:
            return (investment * Decimal(num_months)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

        monthly_rate = rate_decimal / Decimal(12)
        one_plus_r = Decimal(1) + monthly_rate
        future_value = investment * ((one_plus_r**num_months - Decimal(1)) / monthly_rate) * one_plus_r
        return future_value.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    except Exception as e:
        raise ValueError(f"Invalid input for SIP calculation: {e}")

def calculate_fd(principal, annual_interest_rate, tenure_years):
     # ... (ensure this function also uses Decimal correctly if not already) ...
    try:
        principal_amount = Decimal(principal)
        rate_decimal = Decimal(annual_interest_rate) / Decimal(100)
        # Tenure for FD might be float, allow fractional years directly in calculation
        tenure = Decimal(tenure_years)

        if principal_amount <= 0 or rate_decimal < 0 or tenure <= 0:
             raise ValueError("Inputs must be positive.")

        # Simple interest formula: A = P(1 + rt) - adjust if compounding needed
        # Compound Interest: A = P * (1 + r/n)^(nt) - assuming annual compounding (n=1)
        maturity_amount = principal_amount * (Decimal(1) + rate_decimal) ** tenure
        return maturity_amount.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    except Exception as e:
        raise ValueError(f"Invalid input for FD calculation: {e}")


# --- CORRECTED calculate_rd function ---
def calculate_rd(monthly_deposit, annual_interest_rate, tenure_years):
    """Calculates the maturity amount for a Recurring Deposit using Decimal."""
    try:
        # --- Convert inputs to Decimal for precision ---
        principal = Decimal(monthly_deposit) # Ensure it's Decimal
        # Convert annual rate (%) float/int to a Decimal monthly rate
        rate_decimal = Decimal(annual_interest_rate)
        # Convert tenure years (int) to number of months (int is fine for count)
        num_months = int(tenure_years * 12)

        # Input validation
        if principal <= 0 or rate_decimal < 0 or num_months <= 0:
            raise ValueError("Monthly deposit, rate, and tenure must be positive.")

        # Handle zero interest rate case
        if rate_decimal == 0:
            maturity_amount = principal * Decimal(num_months)
            return maturity_amount.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

        # Calculate monthly rate as Decimal
        monthly_rate = (rate_decimal / Decimal(100)) / Decimal(12)

        # --- Calculation using Decimal (Future Value of an Ordinary Annuity) ---
        # FV = P * [((1 + r)^n - 1) / r]
        one_plus_r = Decimal(1) + monthly_rate
        power_term = one_plus_r ** num_months # Exponentiation with Decimal base
        numerator = power_term - Decimal(1)
        denominator = monthly_rate
        maturity_amount = principal * (numerator / denominator)

        # Round the final result to 2 decimal places for currency
        return maturity_amount.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    except (TypeError, ValueError) as e:
        # Catch potential conversion errors or validation errors
        # Reraise as ValueError for consistent handling in the view
        raise ValueError(f"Invalid input for RD calculation: {e}")
    except Exception as e:
        # Catch unexpected errors during calculation
        import traceback
        print("--- RD Calculation Error Traceback ---")
        traceback.print_exc()
        print("--- End Traceback ---")
        raise Exception(f"An unexpected error occurred during RD calculation.") # Re-raise generic exception
# --- END CORRECTED calculate_rd function ---


def estimate_retirement_corpus(current_age, retirement_age, monthly_expenses, inflation_rate, return_rate):
    # ... (ensure this function also uses Decimal correctly if not already) ...
    try:
        c_age = int(current_age)
        r_age = int(retirement_age)
        m_expenses = Decimal(monthly_expenses)
        inf_rate = Decimal(inflation_rate) / Decimal(100)
        ret_rate = Decimal(return_rate) / Decimal(100)

        years_to_retire = r_age - c_age
        if years_to_retire <= 0: raise ValueError("Retirement age must be greater than current age.")

        future_annual_expenses = m_expenses * Decimal(12) * (Decimal(1) + inf_rate)**years_to_retire
        # Calculate corpus needed using inflation-adjusted return rate
        real_return_rate = ((Decimal(1) + ret_rate) / (Decimal(1) + inf_rate)) - Decimal(1)

        if real_return_rate <= 0:
            # If returns don't beat inflation, corpus calculation is problematic (infinite or negative)
            # A simple approach: assume you need enough for ~25-30 years of expenses (adjust as needed)
             return (future_annual_expenses * Decimal(30)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP) # Example: 30 years
            # raise ValueError("Expected return rate must be higher than inflation rate for this calculation.")

        # Assuming expenses needed at the START of retirement year (Perpetuity formula)
        # Corpus = AnnualExpenses / RealReturnRate (simplified)
        corpus = future_annual_expenses / real_return_rate
        return corpus.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    except Exception as e:
        raise ValueError(f"Invalid input for Retirement calculation: {e}")


def estimate_home_loan_eligibility(monthly_income, monthly_obligations, annual_interest_rate, tenure_years):
    # ... (ensure this function also uses Decimal correctly if not already) ...
     try:
        income = Decimal(monthly_income)
        obligations = Decimal(monthly_obligations)
        rate_decimal = Decimal(annual_interest_rate) / Decimal(100)
        num_months = int(tenure_years * 12)

        # Assume bank allows ~50% of disposable income for EMI (FOIR - Fixed Obligation to Income Ratio)
        disposable_income = income - obligations
        max_allowed_emi = disposable_income * Decimal('0.50') # Adjust FOIR % as needed

        if max_allowed_emi <= 0: return Decimal(0)
        if rate_decimal == 0: return Decimal(0) # Cannot calculate loan for 0% rate this way

        monthly_rate = rate_decimal / Decimal(12)
        one_plus_r_n = (Decimal(1) + monthly_rate) ** num_months

        # Calculate Present Value of Annuity (Loan Amount = EMI * [1 - (1 + r)^-n] / r)
        loan_amount = max_allowed_emi * (Decimal(1) - (one_plus_r_n ** Decimal(-1))) / monthly_rate
        return loan_amount.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

     except Exception as e:
        raise ValueError(f"Invalid input for Home Loan Eligibility calculation: {e}")


def calculate_credit_card_balance(current_balance, annual_interest_rate, min_payment_percent, num_months):
    # ... (ensure this function also uses Decimal correctly if not already) ...
     try:
        balance = Decimal(current_balance)
        rate_decimal = Decimal(annual_interest_rate) / Decimal(100)
        min_pay_perc = Decimal(min_payment_percent) / Decimal(100)
        months = int(num_months)

        if balance <= 0: return Decimal(0)
        if months <= 0: return balance.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

        monthly_rate = rate_decimal / Decimal(12)

        # Simulate month by month
        for _ in range(months):
            interest_charged = (balance * monthly_rate).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
            minimum_payment = (balance * min_pay_perc).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
            # Assume a minimum payment floor (e.g., ₹100) if calculated min payment is very low
            minimum_payment = max(minimum_payment, Decimal('100.00')) # Adjust floor as needed

            balance += interest_charged
            # Ensure payment doesn't exceed balance
            payment_made = min(minimum_payment, balance)
            balance -= payment_made
            if balance <= 0:
                balance = Decimal(0)
                break # Stop if paid off

        return balance.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

     except Exception as e:
        raise ValueError(f"Invalid input for Credit Card calculation: {e}")


def calculate_taxable_income(gross_income, total_deductions):
    # ... (ensure this function also uses Decimal correctly if not already) ...
    try:
        income = Decimal(gross_income)
        deductions = Decimal(total_deductions)
        taxable = income - deductions
        # Taxable income can't be negative (usually floor is 0)
        return max(Decimal(0), taxable.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))
    except Exception as e:
        raise ValueError(f"Invalid input for Taxable Income calculation: {e}")


def plan_budget(monthly_income, total_monthly_expenses):
    # ... (ensure this function also uses Decimal correctly if not already) ...
    try:
        income = Decimal(monthly_income)
        expenses = Decimal(total_monthly_expenses)
        savings = (income - expenses).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

        if savings > 0:
            return f"Budget Plan: Income ₹{income:,.2f}, Expenses ₹{expenses:,.2f}. Projected Savings: ₹{savings:,.2f}. Good job!"
        elif savings == 0:
            return f"Budget Plan: Income ₹{income:,.2f}, Expenses ₹{expenses:,.2f}. You're breaking even. Look for ways to save!"
        else:
             deficit = abs(savings)
             return f"Budget Plan: Income ₹{income:,.2f}, Expenses ₹{expenses:,.2f}. Deficit: ₹{deficit:,.2f}. Review expenses urgently!"
    except Exception as e:
        raise ValueError(f"Invalid input for Budget calculation: {e}")


def calculate_net_worth(total_assets, total_liabilities):
    # ... (ensure this function also uses Decimal correctly if not already) ...
    try:
        assets = Decimal(total_assets)
        liabilities = Decimal(total_liabilities)
        net_worth = (assets - liabilities).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        return net_worth
    except Exception as e:
        raise ValueError(f"Invalid input for Net Worth calculation: {e}")