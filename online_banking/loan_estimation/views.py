from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import joblib
import os
from django.conf import settings

@login_required
def loan_estimation(request):
    prediction = None
    error = None
    # Load the model only when the view is called
    model_path = os.path.join(settings.BASE_DIR, 'ml_model', 'loan_model.pkl')
    try:
        model = joblib.load(model_path)
    except FileNotFoundError:
        error = "Model file not found. Please ensure the model has been trained."
        return render(request, 'loan_estimation.html', {'prediction': prediction, 'error': error})

    if request.method == 'POST':
        try:
            age = float(request.POST['age'])
            income = float(request.POST['monthly_income'])
            credit_score = float(request.POST['credit_score'])
            tenure = float(request.POST['tenure'])
            existing_loan = float(request.POST['existing_loan'])
            dependents = int(request.POST['dependents'])
            inputs = [age, income, credit_score, tenure, existing_loan, dependents]
            prediction = model.predict([inputs])[0]
            prediction = round(prediction, 2)
        except ValueError as e:
            error = "Invalid input values"
    return render(request, 'loan_estimation.html', {'prediction': prediction, 'error': error})