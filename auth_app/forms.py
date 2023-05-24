from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate

from auth_app.models import Account
from auth_app.models import *


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(
	    max_length=254, 
		help_text='Required. Add a valid email address.'
	)

    class Meta:
        model = Account
        fields = ('email', 'password1', 'password2', )


class AccountAuthenticationForm(forms.ModelForm):

	password = forms.CharField(label='Password', widget=forms.PasswordInput)

	class Meta:
		model = Account
		fields = ('email', 'password')

	def clean(self):
		if self.is_valid():
			email = self.cleaned_data['email']
			password = self.cleaned_data['password']
			if not authenticate(email=email, password=password):
				raise forms.ValidationError("Invalid login credentials")


class AccountUpdateForm(forms.ModelForm):

	class Meta:
		model = Account
		fields = ('email', )

	def clean_email(self):
		email = self.cleaned_data['email']
		try:
			account = Account.objects.exclude(pk=self.instance.pk).get(email=email)
		except Account.DoesNotExist:
			return email
		raise forms.ValidationError('Email "%s" is already in use.' % account)
