from builtins import super

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Column, Layout, Row, Submit
from django import forms
from pagedown.widgets import PagedownWidget

from .models import Category


class CategoryForm(forms.ModelForm):
    name = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Company Name'}))
    photo = forms.ImageField(label='', widget=forms.ClearableFileInput(attrs={'placeholder': 'Photo'}))
    description = forms.CharField(label='', max_length=1024,
                                  widget=PagedownWidget(attrs={'placeholder': 'Description'}))

    class Meta:
        model = Category
        fields = ('name', 'photo', 'description')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='mt-10 form-group col-md-8 mb-0'),
                Column('photo', css_class='mt-10 form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            'description',
            Submit('submit', 'Submit'),
        )
