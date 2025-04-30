# loan_estimation/views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import joblib
import os
import numpy as np
from django.conf import settings
from .forms import LoanEstimationForm

# --- Model Loading Block ---
MODEL_PATH = os.path.join(settings.BASE_DIR, 'ml_model', 'loan_model.pkl')
MODEL = None
MODEL_LOAD_ERROR = None

try:
    MODEL = joblib.load(MODEL_PATH)
    print("Loan estimation model loaded successfully.")
except FileNotFoundError:
    MODEL_LOAD_ERROR = f"Model file ({MODEL_PATH}) not found. Please ensure 'loan_model.pkl' exists in the 'ml_model' directory after running the training script."
    print(f"Error loading model: {MODEL_LOAD_ERROR}")
except Exception as e:
    MODEL_LOAD_ERROR = f"An error occurred loading the model: {e}"
    print(f"Error loading model: {MODEL_LOAD_ERROR}")
# --- End Model Loading Block ---


# --- View Function ---
@login_required
def loan_estimation(request):
    prediction = None
    # Initialize with an empty form for GET or if POST is invalid
    form = LoanEstimationForm()

    if MODEL_LOAD_ERROR:
        messages.error(request, MODEL_LOAD_ERROR)
        # Render the page showing the model load error
        return render(request, 'loan_estimation/loan_estimation.html', {'model_error': True, 'form': form})

    if request.method == 'POST':
        form = LoanEstimationForm(request.POST) # Populate form with submitted data
        if form.is_valid():
            if MODEL:
                try:
                    # Prepare input features from validated form data
                    data = form.cleaned_data

                    # **CRITICAL FIX**: Ensure this order and the keys exactly match
                    # the 'feature_columns' list in train_model.py and the
                    # field names defined in LoanEstimationForm.
                    input_features = np.array([[
                        float(data['age']),
                        float(data['monthly_income']),
                        float(data['credit_score']),
                        float(data['tenure']),
                        float(data['existing_loan_amount']),
                        float(data['num_of_dependents']) # <= Ensure this key is correct!
                    ]])

                    # Make prediction
                    model_prediction = MODEL.predict(input_features)[0]
                    # Ensure prediction shown to user is never negative
                    prediction = max(0, round(model_prediction, 2))
                    messages.success(request, "Loan amount estimation successful!")

                except KeyError as e:
                     # This error means a key used above (e.g., 'num_of_dependents')
                     # was not found in form.cleaned_data, which shouldn't happen if the form is valid.
                     # Double-check form field names.
                     messages.error(request, f"Data preparation error: Missing key {e}. Please check form definition.")
                     print(f"KeyError during data prep: {e}. Cleaned data: {data}") # Debugging output
                except ValueError as e:
                     messages.error(request, f"Invalid input value for prediction: {e}")
                except Exception as e:
                     # Catch other potential prediction errors
                     messages.error(request, f"An error occurred during prediction: {e}")
                     import traceback
                     print("--- Prediction Error Traceback ---") # Debugging output
                     traceback.print_exc()
                     print("--- End Traceback ---")

            else:
                # This should technically be caught by the MODEL_LOAD_ERROR check above
                messages.error(request, "Prediction model is not available.")
        else:
            # Form is invalid, messages framework will show field errors
            messages.error(request, "Please correct the errors in the form.")
            # The 'form' variable already holds the invalid form instance with errors

    # Prepare context for rendering (works for GET, valid POST, invalid POST)
    context = {
        'form': form, # Pass the form instance (empty, or with data/errors)
        'prediction': prediction, # Pass the prediction result (None or the calculated value)
        'model_error': bool(MODEL_LOAD_ERROR) # Let template know if model failed to load
    }
    return render(request, 'loan_estimation/loan_estimation.html', context)