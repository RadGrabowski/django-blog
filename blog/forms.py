from django import forms
from .models import Comment


class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': 4}))
    bot_catcher = forms.CharField(required=False, widget=forms.HiddenInput)


class CommentForm(forms.ModelForm):
    body = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': 4}))

    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')
