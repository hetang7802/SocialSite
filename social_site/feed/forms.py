from django import forms
from .models import Post,Comment,Like

class NewPostForm(forms.ModelForm):
    class Meta():
        model = Post
        fields = ['description','pic','tags']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['pic'].widget.attrs.update({'enctype': 'multipart/form-data'})
        self.fields['tags'].widget.attrs.update({'placeholder':'enter tags'})


class NewCommentForm(forms.ModelForm):
    class Meta():
        model = Comment
        fields = ['message']
