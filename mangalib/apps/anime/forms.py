from django import forms
from .models import *

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'placeholder': 'Ваш комментарий', 'rows': 4}),
        }

class SearchForm(forms.Form):
    search = forms.CharField(max_length=100, required=False)

class RatingForm(forms.ModelForm):
    star = forms.ModelChoiceField(
        queryset=StarRating.objects.all(),
        widget=forms.RadioSelect(),
        empty_label=None

    )
    class Meta:
        model = Rating
        fields = ['star',]