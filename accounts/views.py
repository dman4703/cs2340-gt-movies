from django.shortcuts import render
from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout
from .forms import CustomUserCreationForm, CustomErrorList
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

# logs out the current user and redirects to the home page.
@login_required
def logout(request):
    auth_logout(request)  # Log the user out.
    return redirect('home.index')  # Redirect to the index page of the home app.

# handles user login functionality.
def login(request):
    template_data = {'title': 'Login'}  # Set the title for the login page.
    if request.method == 'GET':
        # Render the login page when a GET request is received.
        return render(request, 'accounts/login.html', {'template_data': template_data})
    elif request.method == 'POST':
        # Authenticate the user with provided username and password.
        user = authenticate(
            request,
            username=request.POST['username'],
            password=request.POST['password']
        )
        if user is None:
            # If authentication fails, add an error message to the context.
            template_data['error'] = 'The username or password is incorrect.'
            return render(request, 'accounts/login.html', {'template_data': template_data})
        else:
            # If authentication is successful, log the user in.
            auth_login(request, user)
            return redirect('home.index')  # Redirect to home page after successful login.

# handles user registration (signup) functionality.
def signup(request):
    template_data = {'title': 'Sign Up'}  # Set the title for the signup page.
    if request.method == 'GET':
        # Display an empty signup form on GET request.
        template_data['form'] = CustomUserCreationForm()
        return render(request, 'accounts/signup.html', {'template_data': template_data})
    elif request.method == 'POST':
        # Bind the posted data to the signup form, using CustomErrorList for error formatting.
        form = CustomUserCreationForm(request.POST, error_class=CustomErrorList)
        if form.is_valid():
            # If the form is valid, save the new user and redirect to the login page.
            form.save()
            return redirect('accounts.login')
        else:
            # If the form has errors, send the form back to the template to display errors.
            template_data['form'] = form
            return render(request, 'accounts/signup.html', {'template_data': template_data})