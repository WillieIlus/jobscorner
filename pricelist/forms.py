from crispy_forms.bootstrap import InlineRadios
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column
from django.forms import ModelForm

from pricelist.models import Price


class PriceForm(ModelForm):
    class Meta:
        model = Price
        fields = ('company', 'amount', 'description', 'image', 'status', 'negotiable')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('amount', css_class='mt-10 form-group col-md-6 mb-0'),
                Column('company', css_class='mt-10 form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            'description',
            Row(
                Column('image', css_class='mt-10 form-group col-md-5 mb-0'),
                InlineRadios('status', css_class='mt-10 form-group col-md-3 mb-0'),
                InlineRadios('negotiable', css_class='mt-10 form-group col-md-3 mb-0'),
                css_class='form-row'
            ),
            Submit('submit', 'Submit'),
        )
