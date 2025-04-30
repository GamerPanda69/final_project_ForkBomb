# financial_tools/views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .finance_tools import * # Import calculation functions
from .forms import TOOL_FORMS, TOOL_NAMES # Import the forms dictionary and names

@login_required
def tools(request):
    # Dictionary to hold form INSTANCES
    forms_instances = {}
    calculation_result = None
    active_tool = None # Keep track of which tool was submitted/active

    if request.method == 'POST':
        tool_name = request.POST.get('tool_name')
        active_tool = tool_name # Mark the submitted tool as active

        if tool_name in TOOL_FORMS:
            FormClass = TOOL_FORMS[tool_name]
            form_instance = FormClass(request.POST) # Create instance with POST data

            if form_instance.is_valid():
                data = form_instance.cleaned_data
                try:
                    # --- Perform Calculation based on tool_name ---
                    if tool_name == 'emi':
                        result_val = calculate_emi(data['principal'], data['rate'], data['tenure'])
                        calculation_result = f"Calculated EMI: ₹{result_val:,.2f}"
                    elif tool_name == 'sip':
                        result_val = calculate_sip(data['investment'], data['rate'], data['tenure'])
                        calculation_result = f"Estimated SIP Maturity: ₹{result_val:,.2f}"
                    elif tool_name == 'fd':
                        result_val = calculate_fd(data['principal'], data['rate'], data['tenure'])
                        calculation_result = f"Estimated FD Maturity: ₹{result_val:,.2f}"
                    elif tool_name == 'rd':
                        result_val = calculate_rd(data['deposit'], data['rate'], data['tenure'])
                        calculation_result = f"Estimated RD Maturity: ₹{result_val:,.2f}"
                    elif tool_name == 'retirement':
                        result_val = estimate_retirement_corpus(
                            data['current_age'], data['retirement_age'], data['monthly_expenses'],
                            data['inflation_rate'], data['return_rate']
                        )
                        calculation_result = f"Estimated Retirement Corpus Needed: ₹{result_val:,.2f}"
                    elif tool_name == 'home_loan':
                        result_val = estimate_home_loan_eligibility(
                            data['income'], data['obligations'], data['rate'], data['tenure']
                        )
                        calculation_result = f"Estimated Max Home Loan Eligibility: ₹{result_val:,.2f}"
                    elif tool_name == 'credit_card':
                        result_val = calculate_credit_card_balance(
                            data['balance'], data['rate'], data['min_payment'], data['months']
                        )
                        calculation_result = f"Estimated Card Balance after {data['months']} months: ₹{result_val:,.2f}"
                    elif tool_name == 'taxable_income':
                        result_val = calculate_taxable_income(data['gross_income'], data['deductions'])
                        calculation_result = f"Calculated Taxable Income: ₹{result_val:,.2f}"
                    elif tool_name == 'budget':
                        calculation_result = plan_budget(data['income'], data['expenses']) # Returns a string
                    elif tool_name == 'net_worth':
                        result_val = calculate_net_worth(data['assets'], data['liabilities'])
                        calculation_result = f"Calculated Net Worth: ₹{result_val:,.2f}"

                    messages.success(request, "Calculation successful!")
                    # Keep a clean form instance for the active tool after successful calculation
                    forms_instances[tool_name] = FormClass()

                except ValueError as e:
                    messages.error(request, f"Calculation Error: {e}")
                    forms_instances[tool_name] = form_instance # Pass back invalid form
                except Exception as e:
                    messages.error(request, f"An unexpected error occurred: {e}")
                    forms_instances[tool_name] = form_instance # Pass back invalid form
                    import traceback
                    print("--- Calculation Error Traceback ---")
                    traceback.print_exc()
                    print("--- End Traceback ---")

            else:
                # Form is invalid, pass the invalid instance back
                messages.error(request, "Please correct the errors below.")
                forms_instances[tool_name] = form_instance # Store the invalid form instance

        else:
            messages.error(request, "Invalid tool selected.")

    # Populate the rest of the forms_instances dictionary for tools not submitted
    for tool_key, FormCls in TOOL_FORMS.items():
        if tool_key not in forms_instances: # Only add if not already added (e.g., as invalid)
            forms_instances[tool_key] = FormCls() # Add a fresh, empty instance

    context = {
        'forms_instances': forms_instances, # Pass the dictionary of instances
        'calculation_result': calculation_result,
        'active_tool': active_tool,
        'tool_names': TOOL_NAMES # Pass display names for accordion headers
    }
    return render(request, 'financial_tools/tools.html', context)