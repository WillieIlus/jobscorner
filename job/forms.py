from builtins import super

from category.models import Category
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit
from django import forms
from job.models import Job
from location.models import Location


# from taggit import forms


class JobForm(forms.ModelForm):
    title = forms.CharField(label='', required=True, widget=forms.TextInput(attrs={'placeholder': 'Title'}))
    salary = forms.CharField(label='', required=False, widget=forms.TextInput(attrs={'placeholder': 'Salary'}))
    description = forms.CharField(label='', required=True, widget=forms.Textarea(attrs={'placeholder': 'Description'}))
    application_info = forms.CharField(label='', required=False,
                                       widget=forms.Textarea(attrs={'placeholder': 'Application_info'}))
    work_hours = forms.CharField(label='', required=False,
                                 widget=forms.TextInput(attrs={'placeholder': 'Working Hours'}))
    url = forms.CharField(label='', required=False, widget=forms.TextInput(attrs={'placeholder': 'Url'}))
    contact_email = forms.CharField(label='', required=False, widget=forms.TextInput(attrs={'placeholder': 'Email'}))
    location = forms.ModelChoiceField(label='', required=False, queryset=Location.objects.all(),
                                      empty_label="Choose Location")
    category = forms.ModelChoiceField(label='', required=False, queryset=Category.objects.all(),
                                      empty_label="Choose Category")
    remote = forms.BooleanField(label='Remote', required=False, widget=forms.CheckboxInput()),
    tags = forms.CharField(label='', required=False,
                           widget=forms.TextInput(attrs={'placeholder': 'Tags, A comma-separated list of tags'}))

    class Meta:
        model = Job
        # fields = "__all__"
        fields = (
            'title', 'salary', 'description', 'application_info', 'work_hours', 'contact_email', 'url', 'location',
            'category', 'remote', 'tags')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.layout = Layout(
            'title',
            'company',
            'salary',
            'description',
            'application_info',
            Row(
                Column('work_hours', css_class='mt-10 form-group col-md-4 mb-0'),
                Column('contact_email', css_class='mt-10 form-group col-md-8 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('url', css_class='mt-10 form-group col-md-6 mb-0'),
                Column('tags', css_class='mt-10 form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('location', css_class='mt-10 form-group col-md-4 mb-0'),
                Column('category', css_class='mt-10 form-group col-md-4 mb-0'),
                Column('remote', css_id="default-switch", css_class='mt-10 col-md-4 mb-0'),
                css_class='form-row'
            ),
            Submit('submint', 'Submit'),
        )
