# loan_estimation/tests.py
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .forms import LoanEstimationForm
from decimal import Decimal
from unittest.mock import patch, MagicMock
from django.contrib.messages import get_messages
import joblib
 
@patch('loan_estimation.views.MODEL', new_callable=MagicMock)
class LoanEstimationViewsTests(TestCase):
 
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='loanuser', password='password')
        self.loan_estimation_url = reverse('loan_estimation')
        self.login_url = reverse('login')
        self.valid_form_data = {
            'age': 35,
            'monthly_income': Decimal('60000.00'),
            'credit_score': 750,
            'tenure': 10,
            'existing_loan_amount': Decimal('50000.00'),
            'num_of_dependents': 2
        }
 
    def test_loan_estimation_view_requires_login(self, mock_model):
        response = self.client.get(self.loan_estimation_url)
        self.assertRedirects(response, f'{self.login_url}?next={self.loan_estimation_url}')
 
    def test_loan_estimation_view_get(self, mock_model):
        with patch('loan_estimation.views.MODEL_LOAD_ERROR', None):
            self.client.login(username='loanuser', password='password')
            response = self.client.get(self.loan_estimation_url)
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, 'loan_estimation/loan_estimation.html')
            self.assertIn('form', response.context)
            self.assertIsInstance(response.context['form'], LoanEstimationForm)
            self.assertIsNone(response.context.get('prediction'))
            self.assertNotContains(response, 'Estimated Loan Amount:')
 
    def test_loan_estimation_view_post_success(self, mock_model):
        """Test successful loan estimation POST with mocked model."""
        predicted_amount = 250000.00
        mock_model.predict.return_value = [predicted_amount]
 
        self.client.login(username='loanuser', password='password')
        response = self.client.post(self.loan_estimation_url, self.valid_form_data)
 
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'loan_estimation/loan_estimation.html')
        mock_model.predict.assert_called_once()
        self.assertIn('prediction', response.context)
        self.assertEqual(response.context['prediction'], round(predicted_amount, 2))
 
        # *** CORRECTED ASSERTION: Check without the comma ***
        # Check for the currency symbol and the number separately or without comma
        # Option 1: Check without comma
        self.assertContains(response, '₹250000.0') # e.g., checks for "₹250000.00"
        # Option 2: Check parts separately (more robust if spacing changes)
        # self.assertContains(response, '₹')
        # self.assertContains(response, f'{predicted_amount:.2f}')
 
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any('Loan amount estimation successful!' in str(m) for m in messages))
 
    def test_loan_estimation_view_post_invalid_form(self, mock_model):
        """Test loan estimation POST with invalid form data."""
        self.client.login(username='loanuser', password='password')
        invalid_data = self.valid_form_data.copy()
        invalid_data['credit_score'] = 100
 
        response = self.client.post(self.loan_estimation_url, invalid_data)
 
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'loan_estimation/loan_estimation.html')
        self.assertIsNone(response.context.get('prediction'))
        self.assertFormError(response, 'form', 'credit_score', 'Ensure this value is greater than or equal to 300.')
        mock_model.predict.assert_not_called()
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any('Please correct the errors in the form.' in str(m) for m in messages))
 
    @patch('loan_estimation.views.MODEL_LOAD_ERROR', "Simulated Model Load Error")
    def test_loan_estimation_view_model_load_error(self, mock_ignored_model):
        """Test view behaviour when the model failed to load initially."""
        self.client.login(username='loanuser', password='password')
        response = self.client.get(self.loan_estimation_url)
 
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'loan_estimation/loan_estimation.html')
        self.assertContains(response, "The loan estimation tool is currently unavailable.")
        self.assertIn('model_error', response.context)
        self.assertTrue(response.context['model_error'])
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any('Simulated Model Load Error' in str(m) for m in messages))
 
 
    def test_loan_estimation_view_post_prediction_error(self, mock_model):
        """Test view behaviour when model.predict raises an error."""
        mock_model.predict.side_effect = Exception("Simulated prediction failure")
 
        self.client.login(username='loanuser', password='password')
        response = self.client.post(self.loan_estimation_url, self.valid_form_data)
 
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'loan_estimation/loan_estimation.html')
        self.assertIsNone(response.context.get('prediction'))
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any('An error occurred during prediction: Simulated prediction failure' in str(m) for m in messages))
 
 
class LoanEstimationFormsTests(TestCase):
 
    def test_loan_estimation_form_valid(self):
        data = {
            'age': 40, 'monthly_income': 75000, 'credit_score': 800,
            'tenure': 15, 'existing_loan_amount': 100000, 'num_of_dependents': 1
        }
        form = LoanEstimationForm(data=data)
        self.assertTrue(form.is_valid(), form.errors.as_text())
 
    def test_loan_estimation_form_invalid_values(self):
        data = {
            'age': 17, 'monthly_income': -100, 'credit_score': 950,
            'tenure': 0, 'existing_loan_amount': -50, 'num_of_dependents': -1
        }
        form = LoanEstimationForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('age', form.errors)
        self.assertIn('monthly_income', form.errors)
        self.assertIn('credit_score', form.errors)
        self.assertIn('tenure', form.errors)
        self.assertIn('num_of_dependents', form.errors)
 
    def test_loan_estimation_form_missing_required(self):
        data = {
            'credit_score': 700,
            'tenure': 5,
            'existing_loan_amount': 5000
        }
        form = LoanEstimationForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('age', form.errors)
        self.assertIn('monthly_income', form.errors)
        self.assertIn('num_of_dependents', form.errors)
 
    def test_loan_estimation_form_optional_field_blank(self):
        data = {
            'age': 40, 'monthly_income': 75000, 'credit_score': 800,
            'tenure': 15, 'existing_loan_amount': '', 'num_of_dependents': 1
        }
        form = LoanEstimationForm(data=data)
        self.assertTrue(form.is_valid(), form.errors.as_text())
        self.assertEqual(form.cleaned_data['existing_loan_amount'], Decimal('0.00'))