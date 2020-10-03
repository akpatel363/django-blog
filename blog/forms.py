from django import forms
from .models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')
        labels = {'body': 'Comment'}
        widgets = {
            'body': forms.widgets.Textarea(attrs={'rows': 5})
        }


class SearchForm(forms.Form):
    query = forms.CharField(label="Search", widget=forms.widgets.TextInput(
        attrs={'class': 'form-control', 'placeholder': "Search post here..."}))
