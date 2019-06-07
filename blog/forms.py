from builtins import super


from crispy_forms.helper import FormHelper
from crispy_forms.layout import Column, Layout, Row, Submit
from django import forms
from django.forms import ModelForm
from pagedown.widgets import PagedownWidget

from blog.models import STATUS_CHOICES, Comment, Post
from category.models import Category


class PostForm(ModelForm):
    title = forms.CharField(label='', required=True, widget=forms.TextInput(attrs={'placeholder': 'Title'}))
    image = forms.ImageField(label='Image', required=False,
                             widget=forms.ClearableFileInput(attrs={'placeholder': 'Image'}))
    content = forms.CharField(label='', required=True,
                              widget=PagedownWidget(attrs={'placeholder': 'Content'}))
    category = forms.ModelChoiceField(label='', required=False, queryset=Category.objects.all(),
                                      empty_label="Choose Category")
    status = forms.ChoiceField(label='status', required=False, widget=forms.RadioSelect, choices=STATUS_CHOICES)
    tags = forms.CharField(label='', required=False,
                           widget=forms.TextInput(attrs={'placeholder': 'Tags, A comma-separated list of tags'}))

    class Meta:
        model = Post
        fields = ("title", "content", "image", "status", "category", "tags",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'title',
            'image',
            'content',
            Row(
                Column('category', css_class='mt-10 form-group col-md-6 mb-0'),
                Column('status', css_class='mt-10 form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            'tags',
            Submit('submit', 'Submit'),
        )


class CommentForm(ModelForm):
    body = forms.CharField(label='', required=True, widget=forms.TextInput(attrs={'placeholder': 'Comment'}))

    class Meta:
        model = Comment
        fields = ("body",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'body',
            Submit('submit', 'Submit'),
        )
