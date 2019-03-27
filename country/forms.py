from builtins import super

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit
from django import forms
from pagedown.widgets import PagedownWidget

from .models import Country


class CountryForm(forms.ModelForm):
    photo = forms.ImageField(label='', widget=forms.ClearableFileInput(attrs={'placeholder': 'Photo'}))
    description = forms.CharField(label='', max_length=1024,
                                  widget=PagedownWidget(attrs={'placeholder': 'Description'}))
    website = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Website'}))

    class Meta:
        model = Country
        fields = ('name', 'slug', 'photo', 'description')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'name', 'slug',
            'photo',
            'description',
            Submit('submit', 'Save Country Changes'),
        )
