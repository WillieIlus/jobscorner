from builtins import super

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Column, Layout, Row, Submit
from django import forms
from pagedown.widgets import PagedownWidget

from .models import Location


class LocationForm(forms.ModelForm):
    photo = forms.ImageField(label='', widget=forms.ClearableFileInput(attrs={'placeholder': 'Photo'}))
    description = forms.CharField(label='', max_length=1024,
                                  widget=PagedownWidget(attrs={'placeholder': 'Description'}))

    class Meta:
        model = Location
        fields = ('name', 'photo', 'description', 'country')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='mt-10 form-group col-md-6 mb-0'),
                Column('country', css_class='mt-10 form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            'photo',
            'description',
            Submit('submit', 'Submit'),
        )
