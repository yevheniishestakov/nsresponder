from django import forms

class InputForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class UnbindPolicyForm(forms.Form):
    pass

class BindPolicyForm(forms.Form):
    pass