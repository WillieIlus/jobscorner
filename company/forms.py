from builtins import super

from crispy_forms.bootstrap import InlineRadios
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Column, Layout, Row, Submit
from django import forms
# from django.contrib.admin import widgets
from django.forms import inlineformset_factory, ModelForm, formset_factory, widgets
from pagedown.widgets import PagedownWidget

from blog.models import STATUS_CHOICES
from category.models import Category
from company.models import Company, CompanyImage, OpeningHours
from country.models import Country
from location.models import Location


class CompanyForm(ModelForm):
    name = forms.CharField(label='', required=True, widget=forms.TextInput(attrs={'placeholder': 'Company Name'}))
    logo = forms.ImageField(label='Logo', required=False,
                            widget=forms.ClearableFileInput(attrs={'placeholder': 'Logo'}))
    image = forms.ImageField(label='Place Holder Image', required=False,
                             widget=forms.ClearableFileInput(attrs={'placeholder': 'Place holder Image Image'}))
    description = forms.CharField(label='', required=True, max_length=1024,
                                  widget=PagedownWidget(attrs={'placeholder': 'Description'}))
    website = forms.URLField(label='', required=False, widget=forms.TextInput(attrs={'placeholder': 'Company Website'}))
    twitter = forms.CharField(max_length=20, label='', required=False,
                              widget=forms.TextInput(attrs={'placeholder': 'twitter'}))
    location = forms.ModelChoiceField(label='', required=False, queryset=Location.objects.all(),
                                      empty_label="Choose Location")
    category = forms.ModelChoiceField(label='', required=False, queryset=Category.objects.all(),
                                      empty_label="Choose Category")
    email = forms.EmailField(label='', max_length=200, required=True,
                             widget=forms.TextInput(attrs={'placeholder': 'Email'}))
    address = forms.CharField(label='', required=False, widget=forms.TextInput(attrs={'placeholder': 'Address'}))
    status = forms.ChoiceField(label='status', required=False, widget=forms.RadioSelect, choices=STATUS_CHOICES)
    tags = forms.CharField(label='', required=False,
                           widget=forms.TextInput(attrs={'placeholder': 'Tags, A comma-separated list of tags'}))

    class Meta:
        model = Company
        fields = (
            'name', 'logo', 'image', 'description', 'website', 'twitter', 'location', 'category', 'email', "status",
            'address')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'name',
            'logo',
            'image',
            'description',
            Row(
                Column('website', css_class='mt-10 form-group col-md-6 mb-0'),
                Column('twitter', css_class='mt-10 form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('location', css_class='mt-10 form-group col-md-6 mb-0'),
                Column('category', css_class='mt-10 form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('email', css_class='mt-10 form-group col-md-6 mb-0'),
                Column('address', css_class='mt-10 form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('openTime', css_class='mt-10 form-group col-md-6 mb-0'),
                Column('closeTime', css_class='mt-10 form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                InlineRadios('status', css_class='mt-10 form-group col-md-6 mb-0'),
            ),
            Submit('submit', 'Add Your Company'),
        )


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


class CompanyPhotoFormSetHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(CompanyPhotoFormSetHelper, self).__init__(*args, **kwargs)
        self.form_method = 'post'
        self.layout = Layout(
            'img',
            'alt',
        )
        self.render_required_fields = True


WEEKDAYS = [
    (1, "Monday"),
    (2, "Tuesday"),
    (3, "Wednesday"),
    (4, "Thursday"),
    (5, "Friday"),
    (6, "Saturday"),
    (7, "Sunday"),
]


class OpeningHoursForm(ModelForm):
    weekday = forms.ChoiceField(label='', required=False, widget=widgets.RadioSelect, choices=WEEKDAYS)
    from_hour = forms.TimeField(label='From Hour', required=False,
                                widget=widgets.TimeInput(attrs={'placeholder': '6:00:00'}))
    to_hour = forms.TimeField(label='To Hour', required=False,
                              widget=widgets.TimeInput(attrs={'placeholder': '18:00:00'}))

    class Meta:
        model = OpeningHours
        fields = ('weekday', 'from_hour', 'to_hour')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                InlineRadios('weekday', css_class='mt-10 form-group col-md-12 mb-0'),
                Column('from_hour', css_class='mt-10 form-group col-md-6 mb-0'),
                Column('to_hour', css_class='mt-10 form-group col-md-6 mb-0'),
                Submit('submint', 'Submit'),
            ),
        )


OpeningHoursFormset = formset_factory(OpeningHoursForm, extra=6, max_num=7)


class CompanyFilterForm(forms.Form):
    RATING_CHOICES = (
        (1, ''),
        (2, ''),
        (3, ''),
        (4, ''),
        (5, ''),
    )
    category = forms.ModelChoiceField(label="Category", required=False, queryset=Location.objects.all(), )
    country = forms.ModelChoiceField(label="Country", required=False, queryset=Country.objects.all(), )
    location = forms.ModelChoiceField(label="Actor", required=False, queryset=Location.objects.all(), )
    rating = forms.ChoiceField(label="Rating", required=False, choices=RATING_CHOICES,
                               )
