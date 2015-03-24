from django import forms

from Jooglin.lib.forms import Form


class CommentForm(Form):
    comment_text = forms.CharField(widget=forms.Textarea(attrs={'rows': 4, 'cols': 15}))