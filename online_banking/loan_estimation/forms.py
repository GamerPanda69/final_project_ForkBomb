# loan_estimation/forms.py
from django import forms
from decimal import Decimal

class LoanEstimationForm(forms.Form):
    # Field names here are the keys used in form.cleaned_data in the view
    age = forms.IntegerField(min_value=18, max_value=100, label="Age")
    monthly_income = forms.DecimalField(min_value=Decimal('0.01'), label="Monthly Income (₹)")
    credit_score = forms.IntegerField(min_value=300, max_value=900, label="Credit Score")
    tenure = forms.IntegerField(min_value=1, label="Loan Tenure (Years)")
    existing_loan_amount = forms.DecimalField(
        min_value=Decimal('0.00'),
        required=False, # Make it optional
        label="Existing Loan Amount (₹, if any)",
        initial=Decimal('0.00') # Provide an initial default
    )
    # *** CRITICAL FIX: Ensure this field name matches the key used in the view ***
    num_of_dependents = forms.IntegerField(min_value=0, label="Number of Dependents")


    # Add a clean method to handle missing optional field if necessary
    # Although 'required=False' and 'initial' usually suffice for DecimalField
    def clean_existing_loan_amount(self):
        amount = self.cleaned_data.get('existing_loan_amount')
        # If the field is optional and empty, return 0 or None as appropriate for your model
        # Since our model expects a number, returning 0 is safer.
        return amount if amount is not None else Decimal('0.00')