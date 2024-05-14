from django import forms
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

class CustomUserCreationForm(UserCreationForm):
       # Customize this form if necessary.
        class Meta:
           model = CustomUser  # Replace with your custom user model
           fields = ('username', 'email', 'password1', 'password2', 'profileContact', 'profilePicture')
        def clean(self):
            cleaned_data = super().clean()

class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = CustomUser
    def clean(self):
        cleaned_data = super().clean()

class UserProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['profilePicture', 'profileContact', 'username', 'email']

class ApplicantForm(forms.ModelForm):
    class Meta:
        model = Applicant
        fields = '__all__'
        exclude = ['user', 'guardian', 'bursary']

class GuardianForm(forms.ModelForm):
    class Meta:
        model = Guardian
        fields = '__all__'

class InstitutionForm(forms.ModelForm):
    class Meta:
        model = Institution
        fields = '__all__'
        exclude = ['institutionContact']

class ConstituencyForm(forms.ModelForm):
    class Meta:
        model = Constituency
        fields = ['constituencyName']

class WardForm(forms.ModelForm):
    class Meta:
        model = Ward
        fields = '__all__'
        exclude = ['constituency']

class AddBursaryForm(forms.ModelForm):
    class Meta:
        model = Bursary
        fields = '__all__'

class UpdateBursaryForm(forms.ModelForm):
    class Meta:
        model = Bursary
        #fields = ['category', 'status', 'bursaryAmount', 'financialyear', 'dateCreated', 'deadline', 'batchNumber']
        fields = '__all__'

class EditBursaryApplicationForm(forms.ModelForm):
    class Meta:
        model = Bursary
        fields = ['bursaryAmount']

#class ApplicationForm(forms.ModelForm):
    #class Meta:
        #model = Applications
        #fields = '__all__'
        #exclude = ['bursary','date_created', 'deadline']


class InstitutionContactForm(forms.ModelForm):
    class Meta:
        model = Institution
        fields = ['institutionContact']

class FillingDetailsForm(forms.Form):
    #fields for the applicant model
    GENDER = (
        ('Male', 'Male'),
        ('Female', 'Female'),
    )
    LEVEL = (
        ('University', 'University'),
        ('College', 'College'),
        ('Secondary', 'Secondary'),
    )
    STATUS = (
        ('Public', 'Public'),
        ('Private', 'Private'),
    )
    firstName = forms.CharField(max_length=30)
    middleName = forms.CharField(max_length=30)
    lastName = forms.CharField(max_length=30)
    gender = forms.ChoiceField(choices = GENDER)
    email = forms.EmailField(max_length=200)
    contact = forms.CharField(max_length=25)
    DOB = forms.CharField(max_length=200)
    IdOrBirth = forms.FileField()
    studyLevel = forms.ChoiceField(choices = LEVEL)
    admNo = forms.CharField(max_length=20)
    studyYear = forms.CharField(max_length=200)
    course = forms.CharField(max_length=200)
    institutionName = forms.ModelChoiceField(queryset=Institution.objects.all())
    constituencyName = forms.ModelChoiceField(queryset=Constituency.objects.all())
    wardName = forms.ModelChoiceField(queryset=Ward.objects.all())
    #saved in guardian model
    guardianName = forms.CharField(max_length=200) #saved in both applicant and guardian model
    guardianContact = forms.CharField(max_length=25)
    guardianID = forms.FileField()
    guardianGender = forms.ChoiceField(choices = GENDER)
    guardianOccupation = forms.CharField(max_length=200)

class UpdateDetailsForm(forms.ModelForm):
    class Meta:
        model = Applicant
        fields = [
            'firstName', 'middleName', 'lastName', 'gender', 'email', 'contact', 'DOB',
            'IdOrBirth', 'studyLevel', 'admNo', 'studyYear', 'course',
            'institution', 'constituency', 'ward'
        ]

class UpdateGuardianForm(forms.ModelForm):
    class Meta:
        model = Guardian
        fields = '__all__'


