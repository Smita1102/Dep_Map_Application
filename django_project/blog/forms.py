from django import forms
from .models import Question, Choice, SetsAttempted,Book
from django.forms import formset_factory

class BookForm(forms.Form):
    name = forms.CharField(
        label='Add More',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Pre-requisite here'
        })
    )
BookFormset = formset_factory(BookForm, extra=1)