from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Account
from .forms import DepositForm, WithdrawForm

@login_required
def dashboard(request):
    account, created = Account.objects.get_or_create(user=request.user)
    return render(request, 'dashboard.html', {'account': account})

@login_required
def deposit(request):
    account = Account.objects.get(user=request.user)
    if request.method == 'POST':
        form = DepositForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            account.balance += amount
            account.save()
            return redirect('dashboard')
    else:
        form = DepositForm()
    return render(request, 'deposit.html', {'form': form, 'account': account})

@login_required
def withdraw(request):
    account = Account.objects.get(user=request.user)
    if request.method == 'POST':
        form = WithdrawForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            if account.balance >= amount:
                account.balance -= amount
                account.save()
                return redirect('dashboard')
            else:
                form.add_error('amount', 'Insufficient balance')
    else:
        form = WithdrawForm()
    return render(request, 'withdraw.html', {'form': form, 'account': account})