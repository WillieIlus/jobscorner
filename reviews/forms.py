from builtins import super

from crispy_forms.bootstrap import InlineRadios
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Column, Row, Submit
from django.forms import ModelForm, Textarea, RadioSelect

from .models import Review


class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': RadioSelect(),
            'comment': Textarea(attrs={'cols': 40, 'rows': 5}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                InlineRadios('rating')
            ),
            Row(
                Column('comment', css_class='mt-10 form-group col-md-12 mb-0'),
                css_class='form-row'
            ),
            Submit('submit', 'Add Comment')
        )
