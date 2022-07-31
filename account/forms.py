from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from account.models import Account


#user registran form
class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text="Required. Add a valid email address.")

    class Meta:
        model = Account
        fields = ('email','username', 'password1', 'password2') 

    #cleaning the data. add the clean_ and the data to be cleaned and django knows how to clean the data
    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        try:
            account = Account.objects.get(email=email)
        except Exception as e:
            return email
        raise forms.ValidationError(f'Email address {email} already exists')

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            account = Account.objects.get(username=username)
        except Exception as e:
            return username
        raise forms.ValidationError(f'Username {username} already exists')

#user login form
class AccountAuthenticationForm(forms.ModelForm):

    password = forms.CharField(label = 'Password', widget=forms.PasswordInput) #hidden password field

    class Meta:
        model = Account
        fields = ('email', 'password')

    def clean(self):
        if self.is_valid():
            email = self.cleaned_data['email']
            password = self.cleaned_data['password']
            if not authenticate(email=email, password=password):
                raise forms.ValidationError("Invalid Login. Please check if the email or the password is incorrect")

#user account update form
class AccountUpdateForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super(AccountUpdateForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Account
        fields = ('username', 'email', 'name', 'bio', 'hide_email')

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        try:
            account = Account.objects.get(email=email)
            if account.email == self.request.user.email:
                return email
        except Account.DoesNotExist:
            return email
        raise forms.ValidationError(f"Email {email} already in use")

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            account = Account.objects.get(username=username)
            if account.username == self.request.user.username:
                return username
        except Account.DoesNotExist:
            return username
        raise forms.ValidationError(f"Username {username} already in use")

    def save(self, commit=True):
        account = super(AccountUpdateForm, self).save(commit=False)
        account.username = self.cleaned_data['username']
        account.email = self.cleaned_data['email']
        account.name = self.cleaned_data['name']
        account.bio = self.cleaned_data['bio']
        account.hide_email = self.cleaned_data['hide_email']
        if commit:
            account.save()
        return account

#user account image update form
class AccountImageForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['profile_image']

    def save(self, commit=True):
        account = super(AccountImageForm, self).save(commit=False)
        account.profile_image = self.cleaned_data['profile_image']
        if commit:
            account.save()
        return account