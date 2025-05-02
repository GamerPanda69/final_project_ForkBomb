from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from banking.models import Account
from django.contrib.messages import get_messages

class AuthenticationViewsTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.register_url = reverse('register')
        self.login_url = reverse('login')
        self.dashboard_url = reverse('dashboard')
        self.logout_url = reverse('logout')
        self.test_user_data = {
            'username': 'testuser',
            'password': 'testpassword123',
            'password2': 'testpassword123' # UserCreationForm often requires confirmation
        }
        # Create a user for login tests
        self.user = User.objects.create_user(
            username='existinguser',
            password='testpassword123'
        )

    def test_register_view_get(self):
        """Test GET request for registration page."""
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'authentication/register.html')
        self.assertContains(response, 'Register')
        self.assertContains(response, 'csrfmiddlewaretoken') # Check form CSRF

    def test_register_view_post_success(self):
        """Test successful user registration via POST request."""
        # Ensure UserCreationForm fields are used correctly
        form_data = {
            'username': 'newtestuser',
            'password1': 'newpassword123', # Use built-in form field names
            'password2': 'newpassword123'  # Confirmation field
        }
        response = self.client.post(self.register_url, form_data, follow=True) # Follow redirects

        # Check redirection to dashboard
        self.assertRedirects(response, self.dashboard_url, status_code=302, target_status_code=200)
        # Check user creation
        self.assertTrue(User.objects.filter(username='newtestuser').exists())
        new_user = User.objects.get(username='newtestuser')
        # Check user is logged in (response context might have user or check session)
        self.assertEqual(str(response.context['user']), 'newtestuser')
        # Check success message
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Registration successful! Welcome, newtestuser.")
        # Check Account creation signal
        self.assertTrue(Account.objects.filter(user=new_user).exists())

    def test_register_view_post_invalid_data(self):
        """Test registration with invalid data (e.g., mismatched passwords)."""
        form_data = {
            'username': 'invaliduser',
            'password1': 'password123',
            'password2': 'password456' # Mismatched
        }
        response = self.client.post(self.register_url, form_data)
        self.assertEqual(response.status_code, 200) # Should re-render the form
        self.assertTemplateUsed(response, 'authentication/register.html')
        self.assertContains(response, 'The two password fields didn’t match.')
        self.assertFalse(User.objects.filter(username='invaliduser').exists())

    def test_register_view_logged_in_user_redirects(self):
        """Test that a logged-in user accessing register is redirected."""
        self.client.login(username='existinguser', password='testpassword123')
        response = self.client.get(self.register_url, follow=True)
        self.assertRedirects(response, self.dashboard_url, status_code=302, target_status_code=200)

    def test_login_view_get(self):
        """Test GET request for login page."""
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'authentication/login.html')
        self.assertContains(response, 'Login')
        self.assertContains(response, 'csrfmiddlewaretoken')

    def test_login_view_post_success(self):
        """Test successful login."""
        login_data = {'username': 'existinguser', 'password': 'testpassword123'}
        response = self.client.post(self.login_url, login_data, follow=True)
        self.assertRedirects(response, self.dashboard_url, status_code=302, target_status_code=200)
        self.assertEqual(str(response.context['user']), 'existinguser')

    def test_login_view_post_invalid_credentials(self):
        """Test login with incorrect password."""
        login_data = {'username': 'existinguser', 'password': 'wrongpassword'}
        response = self.client.post(self.login_url, login_data)
        self.assertEqual(response.status_code, 200) # Re-renders login form
        self.assertTemplateUsed(response, 'authentication/login.html')
        self.assertContains(response, 'Please enter a correct username and password.') # Check for non-field error
        self.assertNotIn('_auth_user_id', self.client.session) # User should not be logged in

    def test_logout_view(self):
        """Test logout functionality."""
        self.client.login(username='existinguser', password='testpassword123')
        self.assertIn('_auth_user_id', self.client.session) # Verify logged in

        response = self.client.post(self.logout_url, follow=True) # Use POST for LogoutView

        # Check redirection (LOGOUT_REDIRECT_URL is 'login')
        self.assertRedirects(response, self.login_url, status_code=302, target_status_code=200)
        self.assertNotIn('_auth_user_id', self.client.session) # Verify logged out


class AuthenticationSignalsTests(TestCase):

    def test_account_created_on_user_creation(self):
        """Verify the signal creates an Account when a User is created."""
        self.assertFalse(Account.objects.exists()) # No accounts initially
        user = User.objects.create_user(username='signaluser', password='password')
        self.assertTrue(Account.objects.filter(user=user).exists())
        account = Account.objects.get(user=user)
        self.assertEqual(account.balance, 0.00) # Check default balance
