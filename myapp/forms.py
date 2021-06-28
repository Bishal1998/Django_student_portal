from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Homework, Notes, Todo


class CreateNote(forms.ModelForm):
    class Meta:
        model = Notes
        fields = ['title', 'description']


class DateInput(forms.DateInput):
    input_type = "date"


class CreateHomework(forms.ModelForm):
    class Meta:
        model = Homework
        fields = ['subject', 'title', 'description', 'due', 'is_complete']
        widgets = {'due': DateInput()}


class SearchForm(forms.Form):
    search = forms.CharField(max_length=100, label="Enter your Search: ")


class CreateToDo(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ['title', 'is_complete']


class ConversionForm(forms.Form):
    CHOICES = [('length', 'Length'), ('mass', 'Mass')]
    measurement = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)


class ConversionLenghthForm(forms.Form):
    CHOICES = [('yard', 'Yard'), ('foot', 'Foot')]
    input = forms.CharField(required=False, label=False, widget=forms.TextInput(
        attrs={'type': 'number', 'placeholder': 'Enter the number'}
    ))
    measure1 = forms.CharField(
        label='', widget=forms.Select(choices=CHOICES)
    )
    measure2 = forms.CharField(
        label='', widget=forms.Select(choices=CHOICES))


class ConversionMassForm(forms.Form):
    CHOICES = [('pound', 'Pound'), ('kilogram', 'Kilogram')]
    input = forms.CharField(required=False, label=False, widget=forms.TextInput(
        attrs={'type': 'number', 'placeholder': 'Enter the number'}
    ))
    measure1 = forms.CharField(
        label='', widget=forms.Select(choices=CHOICES)
    )
    measure2 = forms.CharField(
        label='', widget=forms.Select(choices=CHOICES)
    )

class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','password1','password2']
