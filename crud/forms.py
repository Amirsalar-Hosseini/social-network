from django import forms
from .models import Post, Comment


class CreateUpdateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'body')


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body', )
        widgets = {
            'body': forms.Textarea(attrs={'class': 'form-control'}),
        }


class ReplyForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body', )


class SearchForm(forms.Form):
    search = forms.CharField()