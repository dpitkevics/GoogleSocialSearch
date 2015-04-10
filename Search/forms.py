from django import forms

import bleach

from Jooglin.lib.forms import Form


class SearchForm(Form):
    query = forms.CharField(label='Search', widget=forms.TextInput(attrs={'autocomplete': 'off', 'class': 'typeahead'}))


class SearchItemForm(forms.ModelForm):
    user = None

    def __init__(self, *args, **kwargs):
        super(SearchItemForm, self).__init__(*args, **kwargs)

    def clean_owner_comment(self):
        owner_comment = self.cleaned_data.get('owner_comment')

        if self.user.has_perm('Search.can_add_basic_html'):
            owner_comment = bleach.clean(owner_comment)
        else:
            owner_comment = bleach.clean(owner_comment, [], [], [])

        return owner_comment

    class Meta:
        widgets = {
            'snippet': forms.Textarea()
        }