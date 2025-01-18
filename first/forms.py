from django import forms

class StringInputForm(forms.Form):
    input_string = forms.CharField(label="Введите строку:", max_length=255)