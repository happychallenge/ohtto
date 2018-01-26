from django import forms
from django.utils.translation import ugettext_lazy as _

from .models import Post, Content, Theme

class PostForm(forms.ModelForm):
    pictures = forms.ImageField(required=False, widget=forms.ClearableFileInput(attrs={'multiple': True}))
    is_public = forms.BooleanField(initial=True, widget=forms.CheckboxInput(attrs={'class': 'js-switch'}))
    text = forms.CharField(label='Short Message', required=False,
            widget=forms.Textarea(attrs={
                    'class': 'post-new-content',
                    'rows': 3,
            })
    )
    class Meta:
        model = Post
        fields = ['theme', 'pictures', 'text',  'is_public']

    def __init__(self, user, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        if self.instance:
            self.fields['theme'].queryset = Theme.objects.filter(author=user)


class PostEditForm(forms.ModelForm):
    pictures = forms.ImageField(widget=forms.HiddenInput())
    is_public = forms.BooleanField(initial=True, widget=forms.CheckboxInput(attrs={'class': 'js-switch'}))
    text = forms.CharField(label='Short Message', required=False,
            widget=forms.Textarea(attrs={
                    'class': 'post-new-content',
                    'rows': 3,
            })
    )
    class Meta:
        model = Post
        fields = ['theme', 'pictures', 'text',  'is_public']

    def __init__(self, user, *args, **kwargs):
        super(PostEditForm, self).__init__(*args, **kwargs)
        if self.instance:
            self.fields['theme'].queryset = Theme.objects.filter(author=user)

class ThemeForm(forms.ModelForm):
    public = forms.BooleanField(label=_("Public"), required=False,
            initial=True, widget=forms.CheckboxInput(attrs={'class': 'js-switch3'}))
    class Meta:
        model = Theme
        fields = ['name', 'public']
