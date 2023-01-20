from django import forms

class EmailSignUpForm(forms.Form):
    email = forms.EmailField(label='Email', max_length=255)
    password = forms.CharField(widget=forms.PasswordInput)