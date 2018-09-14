# import build-in classes for user authentication

from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User

# import our Profile model
from profiles.models import Profile

# import classes from Crispy-Forms app:
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Fieldset, MultiField, Div, Field

# import registration verification code:
from NCG.settings import USER_REG_CODE


# extend the user creation form to include addtl fields and crispyforms:
class UserRegistrationForm(UserCreationForm):
	username = forms.CharField(label='Username')

	password1 = forms.CharField(help_text='Minimum 8 characters',
								label='Password',
								widget=forms.PasswordInput()
								)

	password2 = forms.CharField(help_text='please re-enter',
								label='Password (confirm)',
								widget=forms.PasswordInput()
								)

	verification = forms.CharField(help_text='Contact us for assistance', label='Code')

	class Meta:
		model = User
		fields = ('username','password1', 'password2', 'first_name', 'last_name', 'email')

	def __init__(self, *args, **kwargs):
		super(UserRegistrationForm, self).__init__(*args, **kwargs)

		# crispy stuff
		self.helper = FormHelper()
		self.helper.form_tag = False
		self.helper.form_class = 'form-inline'
		self.helper.layout = Layout(
									Div(
										Field('username'),
										Field('password1'),
										Field('password2'),
										Field('verification')
										),

									Div(
										Div(Field('first_name'), css_class='col-xs-12 col-md-6'),
										Div(Field('last_name'), css_class='col-xs-12 col-md-6'),
										css_class='form-row'
										),

									Div(
										Div(Field('email'), css_class='col-md-12'),
										css_class='form-row'
										),																		
								)


	# extend clean() method to ensure no duplicate username (with varying case)
	# can be created:
	def clean(self):
		cleaned_data = super(UserCreationForm, self).clean()
		username = cleaned_data.get('username')
		if username and User.objects.filter(username__iexact=username).exists():
			self.add_error('username', 'A user with that username already exists.')
		return cleaned_data


	# custom validation on verification field
	def clean_verification(self):
		data = self.cleaned_data['verification']
		if data.lower() not in USER_REG_CODE:
			raise forms.ValidationError('Please check the verification code.')
		return data


class UserUpdateForm(ModelForm):
	def __init__(self, *args, **kwargs):
		super(UserUpdateForm, self).__init__(*args, **kwargs)

		# crispy stuff
		self.helper = FormHelper()
		self.helper.form_tag = False
		self.helper.form_class = 'form-inline'
		self.helper.layout = Layout(
							Div(
								Div(Field('first_name'), css_class='col-md-6'),
								Div(Field('last_name'), css_class='col-md-6'),
								Div(Field('email'), css_class='col-md-12'),
								css_class='form-row'
								),																			
							)

	class Meta:
		model = User
		fields = ('first_name', 'last_name', 'email' )


class UserProfileForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super(UserProfileForm, self).__init__(*args, **kwargs)

		# crispy stuff
		self.helper = FormHelper()
		self.helper.form_tag = False
		self.helper.form_class = 'form-inline'
		self.helper.layout = Layout(
									Div(
										Field('address1'),
										Field('address2')
										),

									Div(

										Div(Field('city'), css_class='col-md-7'),
										Div(Field('state'), css_class='col-md-3'),
										Div(Field('zip'), css_class='col-md-2'),
										css_class='form-row'
										),
									Div(
										Field('phone'),
										),																			
									)
		self.helper.add_input(Submit('Submit', 'Save'))

	class Meta:
		model = Profile
		exclude = ('user',)