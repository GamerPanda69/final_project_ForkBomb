# banking/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Account
from .forms import DepositForm, WithdrawForm
from decimal import Decimal
from django.db import transaction # Import transaction for atomic operations

@login_required
def dashboard(request):
    try:
        # Use related_name 'account' defined in Account model
        account = request.user.account
    except Account.DoesNotExist:
        # This should ideally not happen due to the signal, but handle defensively
        # Option 1: Create it now (if signal failed or user existed before signals)
        account = Account.objects.create(user=request.user)
        messages.info(request, "Your banking account has been created.")
        # Option 2: Show an error and prevent further action (less user-friendly)
        # messages.error(request, "Banking account not found. Please contact support.")
        # return render(request, 'banking/dashboard.html', {'error': True})

    deposit_form = DepositForm()
    withdraw_form = WithdrawForm(account=account) # Pass account for validation

    context = {
        'account': account,
        'deposit_form': deposit_form,
        'withdraw_form': withdraw_form,
    }
    return render(request, 'banking/dashboard.html', context)

@login_required
@transaction.atomic # Ensure deposit operation is atomic
def deposit(request):
    if request.method == 'POST':
        form = DepositForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            try:
                account = request.user.account
                account.balance += amount
                account.save()
                # Add transaction record here if using Transaction model
                messages.success(request, f"₹{amount:.2f} deposited successfully.")
            except Account.DoesNotExist:
                 messages.error(request, "Account not found. Deposit failed.")
            except Exception as e:
                 messages.error(request, f"An error occurred during deposit: {e}")

            return redirect('dashboard')
        else:
            # If form is invalid, redirect back to dashboard and show errors via messages
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{form.fields[field].label}: {error}")
            return redirect('dashboard')

    # If GET request, redirect to dashboard (deposit form is on dashboard)
    return redirect('dashboard')


@login_required
@transaction.atomic # Ensure withdrawal operation is atomic
def withdraw(request):
    try:
        account = request.user.account
    except Account.DoesNotExist:
        messages.error(request, "Account not found. Withdrawal failed.")
        return redirect('dashboard')

    if request.method == 'POST':
        form = WithdrawForm(request.POST, account=account) # Pass account for validation
        if form.is_valid():
            amount = form.cleaned_data['amount']
            # Double check balance just before withdrawal (although form does it too)
            if account.balance >= amount:
                account.balance -= amount
                account.save()
                 # Add transaction record here if using Transaction model
                messages.success(request, f"₹{amount:.2f} withdrawn successfully.")
            else:
                # This case should be caught by form validation, but handle defensively
                messages.error(request, "Insufficient funds.")

            return redirect('dashboard')
        else:
             # If form is invalid, redirect back to dashboard and show errors via messages
            for field, errors in form.errors.items():
                for error in errors:
                     messages.error(request, f"{form.fields[field].label}: {error}")
            return redirect('dashboard')

    # If GET request, redirect to dashboard (withdraw form is on dashboard)
    return redirect('dashboard')