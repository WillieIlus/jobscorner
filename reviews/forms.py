from builtins import super

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Column, Row, Submit
from django import forms
from django.forms import ModelForm, Textarea
from reviews.models import Review


# from crispy_forms.helper import FormHelper
# from crispy_forms.layout import Layout
# from django.forms import ModelForm, Textarea
# from django.forms import ModelForm, forms
# from django.forms import forms

# RATING_CHOICES = (
#     (1, '1'),
#     (2, '2'),
#     (3, '3'),
#     (4, '4'),
#     (5, '5'),
# )

class ReviewForm(ModelForm):
    # RATING_CHOICES = (
    #     (1, '1'),
    #     (2, '2'),
    #     (3, '3'),
    #     (4, '4'),
    #     (5, '5'),
    # )
    # rating = forms.IntegerField(label='',
    #                             widget=forms.RadioSelect(choices=RATING_CHOICES, attrs={'placeholder': 'Rating'}),
    #                             required=True)
    # comment = forms.CharField(label='', widget=forms.Textarea(attrs={'cols': 40, 'rows': 5, 'placeholder': 'Comment'}),
    #                           required=True),

    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'comment': Textarea(attrs={'cols': 40, 'rows': 5}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        # self.helper.form_class = 'form-inline'
        # self.helper.field_template = 'bootstrap4/layout/inline_field.html'
        self.helper.layout = Layout(
            Row(
                Column('rating', css_class='mt-10 form-group col-md-12 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('comment', css_class='mt-10 form-group col-md-12 mb-0'),
                css_class='form-row'
            ),
            Submit('submit', 'Add Comment')
        )
