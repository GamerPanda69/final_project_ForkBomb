# Online Banking

A Django-based online banking system with user auth, deposit/withdraw, finance calculators, and ML-based loan estimation.

# Finance_tools app
# Financial Tools Module

## Purpose

This Python module, `finance_tools`, provides a collection of financial calculation functions designed to help users make informed decisions about loans, investments, savings, and personal finance. The module aims to offer accurate and reliable calculations using the `decimal` module to ensure precision in monetary values.
The module currently includes the following financial calculation tools:

* **EMI Calculator:** Calculates the Equated Monthly Installment for a loan.
* **SIP Calculator:** Estimates the future value of a Systematic Investment Plan (SIP).
* **FD Calculator:** Calculates the maturity amount for a Fixed Deposit (assuming annual compounding).
* **RD Calculator:** Calculates the maturity amount for a Recurring Deposit.
* **Retirement Corpus Estimator:** Estimates the total corpus needed for retirement based on current expenses, inflation, and expected returns.
* **Home Loan Eligibility Estimator:** Estimates the maximum home loan amount a person might be eligible for.
* **Credit Card Balance Calculator:** Simulates the balance of a credit card over a specified number of months, considering interest and minimum payments.
* **Taxable Income Calculator:** Calculates the taxable income by subtracting total deductions from gross income.
* **Budget Planner:** Provides a simple budget analysis based on monthly income and expenses, indicating savings or deficit.
* **Net Worth Calculator:** Calculates the net worth by subtracting total liabilities from total assets.

## How to Run and Test the Module

This module is designed to be used within a Python environment, particularly in a Django project as indicated by the accompanying test file (`tests.py`).

'cd online_banking'
'python manage.py test'
# Authentication appication
 User registration and login
- Secure password hashing
- Session management


### 💰 Banking
- View account balance
- Deposit and withdraw money
- Transaction history

### 📈 Financial Tools
- EMI Calculator
- SIP / FD / RD Calculator
- Retirement Estimator
- Tax, Budget, and Net Worth tools

### 🤖 Loan Estimation (ML)
- Predicts loan eligibility using a trained machine learning model
- Loads `loan_model.pkl` using `joblib` or `pickle`

---

## 🗂 Project Structure

online_banking/
├── manage.py
├── online_banking/
│ ├── settings.py, urls.py, asgi.py, wsgi.py
├── authentication/
│ ├── views.py, models.py,apps.py, urls.py,test.py, templates/
├── banking/
│ ├── views.py, models.py, apps.py, urls.py,test.py templates/
├── financial_tools/
│ ├── views.py, models.py, apps.py, urls.py, finance_tools.py, tests.py(test_financetool), templates/
├── loan_estimation/
│ ├── views.py, models.py, apps.py, urls,py,tests.py, templates/
├── templates/
│ └── base.html
├── static/
│ ├── css/style.css, js/script.js
├── ml_model/
│ ├── loan_model.pkl, train_model.py
├── requirements.txt
└── README.md

## Setup

1. `git clone ...`
2. `cd online_banking`
3. `python -m venv venv && source venv/bin/activate`
4. `pip install -r requirements.txt`
5. `python manage.py migrate`
6. `python manage.py runserver`

Visit `http://127.0.0.1:8000/` and register/login to begin.