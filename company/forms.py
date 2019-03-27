from builtins import super

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Column, Layout, Row, Submit
from django import forms
from django.forms import inlineformset_factory, ModelForm
from pagedown.widgets import PagedownWidget

from category.models import Category
from company.models import Company, CompanyImage
from location.models import Location


class CompanyForm(ModelForm):
    # name = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Company Name'}))
    # logo = forms.ImageField(label='', widget=forms.ClearableFileInput(attrs={'placeholder': 'Logo'}))
    # description = forms.CharField(label='', max_length=1024,
    #                               widget=PagedownWidget(attrs={'placeholder': 'Description'}))
    # website = forms.URLField(label='', widget=forms.TextInput(attrs={'placeholder': 'Company Website'}))
    # twitter = forms.CharField(max_length=20, label='', widget=forms.TextInput(attrs={'placeholder': 'twitter'}))
    # location = forms.ModelChoiceField(label='', queryset=Location.objects.all(), empty_label="Choose Location")
    # category = forms.ModelChoiceField(label='', queryset=Category.objects.all(), empty_label="Choose Category")
    # email = forms.EmailField(label='', max_length=200, widget=forms.TextInput(attrs={'placeholder': 'Email'}))
    # address = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Address'}))
    # openTime = forms.DateField(label='', widget=forms.TimeInput(attrs={'placeholder': 'Open Time'}))
    # closeTime = forms.TimeField(label='', widget=forms.TimeInput(attrs={'placeholder': 'Close Time'}))

    class Meta:
        model = Company
        fields = (
            'name', 'logo', 'description', 'website', 'twitter', 'location', 'category', 'email', 'address')

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.helper = FormHelper()
    #     self.helper.layout = Layout(
    #         'name',
    #         'logo',
    #         'description',
    #         Row(
    #             Column('website', css_class='mt-10 form-group col-md-6 mb-0'),
    #             Column('twitter', css_class='mt-10 form-group col-md-6 mb-0'),
    #             css_class='form-row'
    #         ),
    #         Row(
    #             Column('location', css_class='mt-10 form-group col-md-6 mb-0'),
    #             Column('category', css_class='mt-10 form-group col-md-6 mb-0'),
    #             css_class='form-row'
    #         ),
    #         Row(
    #             Column('email', css_class='mt-10 form-group col-md-6 mb-0'),
    #             Column('address', css_class='mt-10 form-group col-md-6 mb-0'),
    #             css_class='form-row'
    #         ),
    #         Row(
    #             Column('openTime', css_class='mt-10 form-group col-md-6 mb-0'),
    #             Column('closeTime', css_class='mt-10 form-group col-md-6 mb-0'),
    #             css_class='form-row'
    #         ),
    #         Submit('submit', 'Add Your Company'),
    #     )


CompanyPhotoFormSet = inlineformset_factory(Company, CompanyImage, fields=('img', 'alt'),
                                            widgets={'img': forms.FileInput(attrs={
                                                'class': 'form-control',
                                                'placeholder': 'Upload Company Image'
                                            }),
                                                'alt': forms.TextInput(attrs={
                                                    'class': 'form-control',
                                                    'placeholder': 'Describe image'
                                                })},
                                            labels={'img': '',
                                                    'alt': ''},
                                            form=CompanyForm, extra=3)



#
# def __init__(self, *args, **kwargs):
#     super().__init__(*args, **kwargs)
#     self.helper = FormHelper()
#     self.helper.layout = Layout(
#         'img',
#         'alt',
#         Row(
#             Column('img', css_class='mt-10 form-group col-md-8 mb-0'),
#             Column('alt', css_class='mt-10 form-group col-md-4 mb-0'),
#             css_class='form-row'
#         ),
#         Submit('submit', 'Add Your Company'),
#     )