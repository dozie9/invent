__author__ = 'Adelola'

from django import forms

type = (('U','User'), ('S', 'Super User'))

class SignForm(forms.Form):
    username = forms.CharField(max_length=20)
    password = forms.CharField(max_length=20, widget=forms.PasswordInput)
    email = forms.EmailField()
    profile = forms.ChoiceField(choices=type)
    state = forms.CharField(max_length=20)
    local = forms.CharField(max_length=20)

class LoginForm(forms.Form):
    username = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'class':'form-control'}))
    password = forms.CharField(max_length=20, widget=forms.PasswordInput(attrs={'class':'form-control'}))

class SalesForms(forms.Form):
    litres = forms.FloatField(widget=forms.NumberInput(attrs={"id":"calc",
                                                              'class':'form-control',"placeholder":'Enter volume'}))

class UserForm(forms.Form):
    volume = forms.IntegerField()
    perLitre = forms.FloatField()
    amount = forms.FloatField()

