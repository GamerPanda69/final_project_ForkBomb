# banking/tests.py
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Account
from .forms import DepositForm, WithdrawForm
from decimal import Decimal
from django.contrib.messages import get_messages
 
class BankingModelsTests(TestCase):
 
    def test_account_creation_and_str(self):
        """Test Account model creation and string representation."""
        user = User.objects.create_user(username='testbankuser', password='password')
        # Account should be created by signal. Fetch it.
        try:
            account = Account.objects.get(user=user)
        except Account.DoesNotExist:
            self.fail("Account was not created automatically for the user by the signal.")
 
        # Now set the balance for testing the __str__ method with a specific value
        account.balance = Decimal('100.50')
        account.save() # Save the updated balance
 
        self.assertEqual(account.user, user)
        self.assertEqual(account.balance, Decimal('100.50')) # Verify the set balance
        expected_str = f"{user.username}'s Account (Balance: ₹100.50)"
        self.assertEqual(str(account), expected_str)
 
 
class BankingFormsTests(TestCase):
 
    def setUp(self):
        # User creation triggers the signal to create the Account
        self.user = User.objects.create_user(username='formuser', password='password')
        # Get the automatically created account
        try:
            self.account = Account.objects.get(user=self.user)
        except Account.DoesNotExist:
             # This should not happen if signals are working, but fail test if it does
            self.fail("Account was not created automatically for the user.")
        # Set the desired balance for tests
        self.account.balance = Decimal('500.00')
        self.account.save()
 
    def test_deposit_form_valid(self):
        """Test DepositForm with valid data."""
        form = DepositForm(data={'amount': Decimal('50.25')})
        self.assertTrue(form.is_valid())
 
    def test_deposit_form_invalid_zero(self):
        """Test DepositForm with zero amount."""
        form = DepositForm(data={'amount': Decimal('0.00')})
        self.assertFalse(form.is_valid())
        self.assertIn('Ensure this value is greater than or equal to 0.01.', form.errors['amount'])
 
    def test_deposit_form_invalid_negative(self):
        """Test DepositForm with negative amount."""
        form = DepositForm(data={'amount': Decimal('-10.00')})
        self.assertFalse(form.is_valid())
        self.assertIn('Ensure this value is greater than or equal to 0.01.', form.errors['amount'])
 
    def test_withdraw_form_valid(self):
        """Test WithdrawForm with valid amount and sufficient funds."""
        form = WithdrawForm(data={'amount': Decimal('100.00')}, account=self.account)
        self.assertTrue(form.is_valid())
 
    def test_withdraw_form_invalid_zero(self):
        """Test WithdrawForm with zero amount."""
        form = WithdrawForm(data={'amount': Decimal('0.00')}, account=self.account)
        self.assertFalse(form.is_valid())
        self.assertIn('Ensure this value is greater than or equal to 0.01.', form.errors['amount'])
 
    def test_withdraw_form_insufficient_funds(self):
        """Test WithdrawForm with amount exceeding balance."""
        form = WithdrawForm(data={'amount': Decimal('600.00')}, account=self.account)
        self.assertFalse(form.is_valid())
        self.assertIn('Insufficient funds.', form.errors['amount'])
 
    def test_withdraw_form_missing_account(self):
        """Test WithdrawForm initialization without account (should ideally not happen)."""
        form = WithdrawForm(data={'amount': Decimal('10.00')}) # No account passed
        self.assertFalse(form.is_valid())
        self.assertTrue('amount' in form.errors or '__all__' in form.errors)
 
 
class BankingViewsTests(TestCase):
 
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='viewuser', password='password')
        # Account automatically created by signal, get it and set balance
        self.account = Account.objects.get(user=self.user)
        self.account.balance = Decimal('1000.00')
        self.account.save()
 
        self.dashboard_url = reverse('dashboard')
        self.deposit_url = reverse('deposit')
        self.withdraw_url = reverse('withdraw')
        self.login_url = reverse('login')
 
    def test_dashboard_view_requires_login(self):
        """Test dashboard view redirects unauthenticated users."""
        response = self.client.get(self.dashboard_url)
        self.assertRedirects(response, f'{self.login_url}?next={self.dashboard_url}')
 
    def test_dashboard_view_authenticated_user(self):
        """Test dashboard view for logged-in user."""
        self.client.login(username='viewuser', password='password')
        response = self.client.get(self.dashboard_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'banking/dashboard.html')
        self.assertContains(response, f'Current Balance')
        # Check balance rendering WITHOUT comma for simplicity
        self.assertContains(response, f'₹1000.00')
        self.assertEqual(response.context['account'], self.account)
        self.assertIsInstance(response.context['deposit_form'], DepositForm)
        self.assertIsInstance(response.context['withdraw_form'], WithdrawForm)
 
    def test_deposit_view_requires_login(self):
        """Test deposit view redirects unauthenticated users."""
        response = self.client.post(self.deposit_url, {'amount': '50'})
        self.assertRedirects(response, f'{self.login_url}?next={self.deposit_url}')
 
    def test_deposit_view_get_redirects(self):
        """Test GET request to deposit view redirects to dashboard."""
        self.client.login(username='viewuser', password='password')
        response = self.client.get(self.deposit_url)
        self.assertRedirects(response, self.dashboard_url)
 
    def test_deposit_view_post_success(self):
        """Test successful deposit via POST."""
        self.client.login(username='viewuser', password='password')
        initial_balance = self.account.balance
        deposit_amount = Decimal('150.75')
        response = self.client.post(self.deposit_url, {'amount': str(deposit_amount)}, follow=True)
 
        self.assertRedirects(response, self.dashboard_url, status_code=302, target_status_code=200)
        self.account.refresh_from_db() # Get updated balance
        self.assertEqual(self.account.balance, initial_balance + deposit_amount)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), f"₹{deposit_amount:.2f} deposited successfully.")
 
    def test_deposit_view_post_invalid_form(self):
        """Test deposit POST with invalid data."""
        self.client.login(username='viewuser', password='password')
        initial_balance = self.account.balance
        response = self.client.post(self.deposit_url, {'amount': '-50'}, follow=True)
 
        self.assertRedirects(response, self.dashboard_url, status_code=302, target_status_code=200)
        self.account.refresh_from_db()
        self.assertEqual(self.account.balance, initial_balance) # Balance should not change
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any('Ensure this value is greater than or equal to 0.01.' in str(m) for m in messages))
 
    def test_withdraw_view_requires_login(self):
        """Test withdraw view redirects unauthenticated users."""
        response = self.client.post(self.withdraw_url, {'amount': '50'})
        self.assertRedirects(response, f'{self.login_url}?next={self.withdraw_url}')
 
    def test_withdraw_view_get_redirects(self):
        """Test GET request to withdraw view redirects to dashboard."""
        self.client.login(username='viewuser', password='password')
        response = self.client.get(self.withdraw_url)
        self.assertRedirects(response, self.dashboard_url)
 
    def test_withdraw_view_post_success(self):
        """Test successful withdrawal via POST."""
        self.client.login(username='viewuser', password='password')
        initial_balance = self.account.balance
        withdraw_amount = Decimal('200.50')
        response = self.client.post(self.withdraw_url, {'amount': str(withdraw_amount)}, follow=True)
 
        self.assertRedirects(response, self.dashboard_url, status_code=302, target_status_code=200)
        self.account.refresh_from_db() # Get updated balance
        self.assertEqual(self.account.balance, initial_balance - withdraw_amount)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), f"₹{withdraw_amount:.2f} withdrawn successfully.")
 
    def test_withdraw_view_post_insufficient_funds(self):
        """Test withdrawal POST with insufficient funds."""
        self.client.login(username='viewuser', password='password')
        initial_balance = self.account.balance
        withdraw_amount = Decimal('1200.00') # More than balance
        response = self.client.post(self.withdraw_url, {'amount': str(withdraw_amount)}, follow=True)
 
        self.assertRedirects(response, self.dashboard_url, status_code=302, target_status_code=200)
        self.account.refresh_from_db()
        self.assertEqual(self.account.balance, initial_balance) # Balance should not change
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any('Insufficient funds.' in str(m) for m in messages))