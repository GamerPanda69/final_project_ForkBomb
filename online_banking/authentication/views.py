# authentication/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages # Import messages

def register(request):
    if request.user.is_authenticated:
        return redirect('dashboard') # Redirect logged-in users away

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user) # Log the user in immediately after registration
            messages.success(request, f"Registration successful! Welcome, {user.username}.")
            return redirect('dashboard') # Redirect to dashboard (LOGIN_REDIRECT_URL handles this too)
        else:
            # Pass error messages to the template
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = UserCreationForm()
    return render(request, 'authentication/register.html', {'form': form})

# We are using the built-in LoginView and LogoutView directly in urls.py
# No need for CustomLoginView unless specific customization is required.