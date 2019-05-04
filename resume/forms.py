# from builtins import super
#
# from crispy_forms.helper import FormHelper
# from crispy_forms.layout import Layout, Row, Column, Submit
# from django import forms
#
# from category.models import Category
# from job.models import Job
# from location.models import Location
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit
from django import forms
from location.models import Location

from .models import Profile, Skill, Experience, Education


class ProfileForm(forms.ModelForm):
    bio = forms.CharField(label='', required=True, widget=forms.Textarea(attrs={
        'placeholder': 'Give a good description about yourself, help people understand your strength, and skills'}))
    location = forms.ModelChoiceField(label='', required=False, queryset=Location.objects.all(),
                                      empty_label="Choose Location")
    birth_date = forms.DateField(label='', required=True, widget=forms.DateInput(attrs={'placeholder': 'Birth Date'}))
    thumbnail = forms.ImageField(label='', required=True, widget=forms.FileInput(attrs={'placeholder': 'Thumbnail'}))
    phone = forms.CharField(label='', required=True, widget=forms.NumberInput(attrs={'placeholder': 'phone'}))
    website = forms.CharField(label='', required=True, widget=forms.TextInput(attrs={'placeholder': 'website'}))
    facebook = forms.CharField(label='', required=True, widget=forms.TextInput(attrs={'placeholder': 'facebook'}))
    instagram = forms.CharField(label='', required=True, widget=forms.TextInput(attrs={'placeholder': 'instagram'}))
    twitter = forms.CharField(label='', required=True, widget=forms.TextInput(attrs={'placeholder': 'twitter'}))
    linkedin = forms.CharField(label='', required=True, widget=forms.TextInput(attrs={'placeholder': 'linkedin'}))
    google = forms.CharField(label='', required=True, widget=forms.TextInput(attrs={'placeholder': 'google'}))
    pinterest = forms.CharField(label='', required=True, widget=forms.TextInput(attrs={'placeholder': 'pinterest'}))
    tags = forms.CharField(label='', required=False,
                           widget=forms.TextInput(attrs={'placeholder': 'Tags, A comma-separated list of tags'}))

    class Meta:
        model = Profile
        fields = ('bio', 'location', 'birth_date', 'thumbnail', 'phone', 'website', 'facebook', 'instagram', 'twitter',
                  'linkedin', 'google', 'pinterest')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.layout = Layout(
            'bio',
            Row(
                Column('location', css_class='mt-10 form-group col-md-4 mb-0'),
                Column('birth_date', css_class='mt-10 form-group col-md-8 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('thumbnail', css_class='mt-10 form-group col-md-4 mb-0'),
                Column('phone', css_class='mt-10 form-group col-md-8 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('phone', css_class='mt-10 form-group col-md-4 mb-0'),
                Column('website', css_class='mt-10 form-group col-md-8 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('facebook', css_class='mt-10 form-group col-md-4 mb-0'),
                Column('instagram', css_class='mt-10 form-group col-md-4 mb-0'),
                Column('twitter', css_class='mt-10 form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('google', css_class='mt-10 form-group col-md-4 mb-0'),
                Column('linkedin', css_class='mt-10 form-group col-md-4 mb-0'),
                Column('pinterest', css_class='mt-10 form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            Submit('submint', 'Submit'),
        )


class SkillForm(forms.ModelForm):
    SKILL_LEVELS = (
        (None, 'unknown'),
        ('B', 'beginner'),
        ('S', 'skilled'),
        ('A', 'advanced'),
        ('E', 'expert'),
    )

    name = forms.CharField(label='', required=True, widget=forms.TextInput(attrs={'placeholder': 'Skill Name'}))
    description = forms.CharField(label='', required=True, widget=forms.Textarea(attrs={
        'placeholder': 'short description'}))
    level = forms.ChoiceField(label='', required=True, widget=forms.RadioSelect, choices=SKILL_LEVELS)
    tags = forms.CharField(label='', required=True,
                           widget=forms.TextInput(attrs={'placeholder': 'A comma-separated list of tags.'}))

    class Meta:
        model = Skill
        fields = ('name', 'description', 'level', 'tags')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.layout = Layout(
            'name',
            Row(
                Column('level', css_class='mt-10 form-group col-md-3 mb-0'),
                Column('description', css_class='mt-10 form-group col-md-9 mb-0'),
                css_class='form-row'
            ),
            'tags',
            Submit('submint', 'Submit'),
        )


class EducationForm(forms.ModelForm):
    major = forms.CharField(label='', required=True, widget=forms.TextInput(attrs={'placeholder': 'Major'}))
    school = forms.CharField(label='', required=True, widget=forms.TextInput(attrs={'placeholder': 'School Name'}))
    school_url = forms.CharField(label='', required=True, widget=forms.TextInput(attrs={'placeholder': 'School Url'}))
    start_date = forms.CharField(label='', required=True, widget=forms.TextInput(attrs={'placeholder': 'Start Date'}))
    completion_date = forms.CharField(label='', required=True,
                                      widget=forms.TextInput(attrs={'placeholder': 'Completion Date'}))
    summary = forms.CharField(label='', required=True, widget=forms.Textarea(attrs={
        'placeholder': 'Summary'}))
    is_current = forms.BooleanField(label='', required=False,
                                    widget=forms.CheckboxInput(attrs={'placeholder': 'Is Current'}))

    class Meta:
        model = Education
        fields = ['school', 'school_url', 'major', 'result', 'start_date', 'completion_date', 'summary', 'is_current']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.layout = Layout(
            'major',
            Row(
                Column('school', css_class='mt-10 form-group col-md-6 mb-0'),
                Column('school_url', css_class='mt-10 form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('start_date', css_class='mt-10 form-group col-md-6 mb-0'),
                Column('completion_date', css_class='mt-10 form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            'summary',
            'is_current',

            Submit('submit', 'Submit'),
        )


class ExperienceForm(forms.ModelForm):
    role = forms.CharField(label='', required=True, widget=forms.TextInput(attrs={'placeholder': 'Role'}))
    company = forms.CharField(label='', required=True, widget=forms.TextInput(attrs={'placeholder': 'Company Name'}))
    company_url = forms.CharField(label='', required=True, widget=forms.TextInput(attrs={'placeholder': 'Company Url'}))
    start_date = forms.CharField(label='', required=True, widget=forms.TextInput(attrs={'placeholder': 'Start Date'}))
    completion_date = forms.CharField(label='', required=True,
                                      widget=forms.TextInput(attrs={'placeholder': 'Completion Date'}))
    description = forms.CharField(label='', required=True, widget=forms.Textarea(attrs={
        'placeholder': 'short description'}))
    is_current = forms.BooleanField(label='', required=False,
                                    widget=forms.CheckboxInput(attrs={'placeholder': 'Is Current'}))

    class Meta:
        model = Experience
        fields = ['role', 'company', 'company_url', 'start_date', 'completion_date', 'description', 'is_current']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.layout = Layout(
            'role',
            Row(
                Column('company', css_class='mt-10 form-group col-md-6 mb-0'),
                Column('company_url', css_class='mt-10 form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('start_date', css_class='mt-10 form-group col-md-6 mb-0'),
                Column('completion_date', css_class='mt-10 form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            'description',
            'is_current',
            Submit('submint', 'Submit'),
        )
