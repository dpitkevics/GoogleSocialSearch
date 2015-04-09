from django import forms

from Jooglin.lib.forms import Form


class SearchForm(Form):
    query = forms.CharField(label='Search', widget=forms.TextInput(attrs={'autocomplete': 'off', 'class': 'typeahead'}))


class SearchItemForm(forms.ModelForm):
    class Meta:
        widgets = {
            'snippet': forms.Textarea()
        }