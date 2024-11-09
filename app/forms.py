from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm, AuthenticationForm
from .models import *
from django.forms.widgets import PasswordInput, TextInput, EmailInput

from phonenumber_field.formfields import PhoneNumberField

class RegistsForm(UserCreationForm):
  username = forms.CharField(widget=TextInput(attrs={'class':'textbox','placeholder':'Username'}))
  email = forms.EmailField(widget=EmailInput(attrs={'class':'textbox','placeholder':'Email'}))
  password1 = forms.CharField(widget=PasswordInput(attrs={'class':'textbox','id':'password','placeholder':'Password'}))
  password2 = forms.CharField(widget=PasswordInput(attrs={'class':'textbox','id':'password','placeholder':'Confirm Password'}))
  class Meta:
    model = Account
    fields = ["username","email","password1","password2"]
    
class LoginForm(AuthenticationForm):
  username = forms.CharField(required=True,widget=TextInput(attrs={'class':'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-600 dark:border-gray-500 dark:placeholder-gray-400 dark:text-white','placeholder':'Username'}))
  password = forms.CharField(required=True,widget=PasswordInput(attrs={'class':'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-600 dark:border-gray-500 dark:placeholder-gray-400 dark:text-white','id':'password','placeholder':'Password'}))
  class Meta:
    model = Account
    fields = ["username","password"]
    
class UpdateUserProfile(forms.ModelForm):
  username = forms.CharField(max_length=100,required=True,label="Change username" ,widget=TextInput(attrs={"class":"mt-1 block w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition duration-300 ease-in-out"}))
  first_name = forms.CharField(max_length=100,required=False,label="Change first name")
  last_name = forms.CharField(max_length=100,required=False,label="Change last name")
  email = forms.EmailField(max_length=100, required=True,label="Change Email")
  phonenumber = PhoneNumberField()
  
  class Meta:
    model = Account
    fields = ["username","first_name", "last_name","email","phonenumber"]
    
class PasswordChangeForm(PasswordChangeForm):
  class Meta:
    model = Account
    fields = ['old_password','new_password1','new_password2']