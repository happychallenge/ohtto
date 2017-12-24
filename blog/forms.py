from django import forms


from .models import Post, Content, Theme

class PostForm(forms.ModelForm):
    pictures = forms.FileField(required=False, widget=forms.ClearableFileInput(attrs={'multiple': True}))
    is_published = forms.BooleanField(initial=True, widget=forms.CheckboxInput(attrs={'class': 'js-switch'}))
    text = forms.CharField(label='Short Message', required=False,
            widget=forms.Textarea(attrs={
                    'class': 'post-new-content',
                    'rows': 3,
            })
    )
    class Meta:
        model = Post
        fields = ['theme', 'pictures', 'text',  'is_published']

    def __init__(self, user, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        if self.instance:
            self.fields['theme'].queryset = Theme.objects.filter(author=user)
