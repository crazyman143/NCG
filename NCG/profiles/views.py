from django.shortcuts import render, redirect

# decorator to enforce authentication before loading view
from django.contrib.auth.decorators import login_required


# import forms for registration.  import built-in auth classes
from django.contrib.auth import login, authenticate

# import built-in form for user creation
from django.contrib.auth.forms import UserCreationForm

# import my forms
from .forms import UserRegistrationForm, UserProfileForm

# built-in messaging framework
from django.contrib import messages

# for now we're creating our own password reset 
# view. eventually need to either A: use the built-in views
# for user auth completely or B: build our own into the 'profiles'
# app bc its getting confusing whats what. 
# currently registration and profile edit is handled here, but the
# rest (login/logout/password reset etc) is handled by default auth views.
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm

# import default authentication views
from django.contrib.auth.views import (
    LoginView,
    LogoutView,
    PasswordResetView,
    PasswordResetDoneView,
    PasswordChangeView,
    PasswordChangeDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView
    )

# need this to override reverse_url in extended class
from django.urls import reverse_lazy

# Create your views here.


class LoginView(LoginView):
	template_name = 'profiles/login.html'



class LogoutView(LoginView):
	pass

class PasswordChangeView(PasswordChangeView):
	template_name = 'profiles/password_change_form.html'
	# have to override this because we need namespace included
	success_url = reverse_lazy('profiles:password_change_done')


def password_change_done(request):
		message = '<strong>Success:</strong> Password Changed.'
		messages.add_message(request, messages.SUCCESS, message)
		return redirect('profiles:change_password')


class PasswordResetView(PasswordResetView):
	email_template_name = 'profiles/password_reset_email.html'
	subject_template_name = 'profiles/password_reset_subject.txt'
	template_name = 'profiles/password_reset_form.html'
	success_url = reverse_lazy('profiles:password_reset_done')


def password_reset_done(request):
		message = '<strong>Success:</strong> Please check for an email with further instructions.'
		messages.add_message(request, messages.SUCCESS, message)
		return redirect('profiles:password_reset')


def index(request):

	# return a render. pass the request and template
	return render(request, 'profiles/profile.html')

	
def register(request):

	# dictionary to hold output values
	output = dict()

	# if data was submitted
	if request.method == 'POST':
		
		# populate the forms with POST data
		user_form 		=	UserRegistrationForm(request.POST)
		profile_form	=	UserProfileForm(request.POST)

		# if forms are valid
		if user_form.is_valid() and profile_form.is_valid():

			# save user form, create new user
			user_form.save()

			# authenticate the new user based on the form data. 
			# log in the user
			user = authenticate(username=user_form.cleaned_data['username'], password=user_form.cleaned_data['password1'],)
			login(request, user)
			
			# populate our profile form with POST data. Retrieve the instance that is tied to the logged in user. 
			profile_form	=	UserProfileForm(request.POST, instance=request.user.profile)
			profile_form.save()

			# user creation, login, and profile creation done. return user somewhere.
			return redirect('/cemex')

			
	# if forms werent submitted, build them.  
	else:
	
		user_form 		= UserRegistrationForm()
		profile_form 	= UserProfileForm()
	
	# populate the dictionary
	output['user_form'] = user_form
	output['profile_form'] = profile_form

	return render(request, 'profiles/register.html', output)
	
	
def edit(request):

	# dictionary to hold output values
	output = dict()

	# if data was submitted
	if request.method == 'POST':
		
		# populate Profile Form with POST data and instance from authenticated user
		profile_form 		=	UserProfileForm(request.POST, instance=request.user.profile)

		# if that form is valid
		if profile_form.is_valid():

			# save the form
			profile_form.save()

			# user feedback
			message = '<strong>Success:</strong> Your profile was saved.'
			messages.add_message(request, messages.SUCCESS, message)


	# if no data submitted, populate profile form and return to the user.  
	else:
		profile_form	=	UserProfileForm(instance=request.user.profile)
	
	# populate the dictionary
	output['profile_form'] = profile_form

	return render(request, 'profiles/edit.html', output)


def change_password(request):
	if request.method == 'POST':
		form = PasswordChangeForm(request.user, request.POST)
		if form.is_valid():
			user = form.save()
			update_session_auth_hash(request, user)  # Important!

			message = '<strong>Success:</strong> Your password was changed.'
			messages.add_message(request, messages.SUCCESS, message)

			return redirect('profiles:edit')
	else:
		form = PasswordChangeForm(request.user)
	return render(request, 'profiles/change_password.html', {'form': form})