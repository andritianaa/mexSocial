from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.forms import fields
from authy.models import Profile

def ForbiddenUsers(value):
	forbidden_users = ['admin', 'css', 'js', 'authenticate', 'login', 'logout', 'administrator', 'root',
	'email', 'user', 'join', 'sql', 'static', 'python', 'delete']
	if value.lower() in forbidden_users:
		raise ValidationError("Nom d'utilisateur invalide.")

def InvalidUser(value):
	if '@' in value or '+' in value or '-' in value:
		raise ValidationError("Le nom d'utilisateur ne doit pas contenir le charactères: @ , - , + ")

def UniqueEmail(value):
	if User.objects.filter(email__iexact=value).exists():
		raise ValidationError('Un compte avec cet adresse email existe déjà')

def UniqueUser(value):
	if User.objects.filter(username__iexact=value).exists():
		raise ValidationError("Ce nom d'utilisateur est déjà utilisé")

class SignupForm(forms.ModelForm):
	username = forms.CharField(widget=forms.TextInput(attrs={'class': 'input-text'}), max_length=30, required=True,)
	email   = forms.CharField(widget=forms.EmailInput(), max_length=100, required=False)
	password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input-text'}))
	confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input-text'}), required=True, label="Confirmation de mot de passe")

	class Meta:
		model = User
		fields = ('username', 'email', 'password')
  
	def __init__(self, *args, **kwargs):
		super(SignupForm, self).__init__(*args, **kwargs)
		self.fields['username'].validators.append(ForbiddenUsers)
		self.fields['username'].validators.append(InvalidUser)
		self.fields['username'].validators.append(UniqueUser)
		self.fields['email'].validators.append(UniqueEmail)

	def clean(self):
		super(SignupForm, self).clean()
		password = self.cleaned_data.get('password')
		confirm_password = self.cleaned_data.get('confirm_password')

		if password != confirm_password:
			self._errors['password'] = self.error_class(['Les mots de passe ne correspondent pas.'])
		return self.cleaned_data

class ChangePasswordForm(forms.ModelForm):
	id = forms.CharField(widget=forms.HiddenInput())
	old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input-text'}), label="Old password", required=True)
	new_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input-text'}), label="New password", required=True)
	confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input-text'}), label="Confirm new password", required=True)

	class Meta:
		model = User
		fields = ('id', 'old_password', 'new_password', 'confirm_password')

	def clean(self):
		super(ChangePasswordForm, self).clean()
		id = self.cleaned_data.get('id')
		old_password = self.cleaned_data.get('old_password')
		new_password = self.cleaned_data.get('new_password')
		confirm_password = self.cleaned_data.get('confirm_password')
		user = User.objects.get(pk=id)
		if not user.check_password(old_password):
			self._errors["Erreur ancien mot de passe"] =self.error_class(["L'ancien mot de passe n'est pas valide"])
		if new_password != confirm_password:
			self._errors['Erreur de correspondance'] =self.error_class(['Les mots de passe ne correspondent pas.'])
		return self.cleaned_data

class EditProfileForm(forms.ModelForm):
	picture = forms.ImageField(required=False)
	first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'input-text'}), max_length=50, required=False )
	last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'input-text'}), max_length=50, required=False)
	location = forms.CharField(widget=forms.TextInput(attrs={'class': 'input-text'}), max_length=25, required=False)
	url = forms.URLField(widget=forms.TextInput(attrs={'class': 'input-text'}), max_length=60, required=False)
	profile_info = forms.CharField(widget=forms.TextInput(attrs={'class': 'input-text'}), max_length=260, required=False)

	class Meta:
		model = Profile
		fields = ('picture', 'first_name', 'last_name', 'location', 'url', 'profile_info')
  
class EditPictureForm(forms.ModelForm):
	picture = forms.ImageField(required=False)

	class Meta:
		model = Profile
		fields = ('picture',)

class EditNameForm(forms.ModelForm):
	first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'input-text'}), max_length=50, required=False )
	last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'input-text'}), max_length=50, required=False)

	class Meta:
		model = Profile
		fields = ('first_name', 'last_name')
  
class EditLocationForm(forms.ModelForm):
	location = forms.CharField(widget=forms.TextInput(attrs={'class': 'input-text'}), max_length=25, required=False)

	class Meta:
		model = Profile
		fields = ('location',)
  
  
class EditUrlForm(forms.ModelForm):
	url = forms.URLField(widget=forms.TextInput(attrs={'class': 'input-text'}), max_length=60, required=False)

	class Meta:
		model = Profile
		fields = ('url',)
  
class EditProfile_infoForm(forms.ModelForm):
	profile_info = forms.CharField(widget=forms.TextInput(attrs={'class': 'input-text'}), max_length=260, required=False)

	class Meta:
		model = Profile
		fields = ('profile_info',)
  