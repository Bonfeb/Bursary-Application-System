import django_filters
from django_filters import DateFilter
from .models import *

class ApplicantFilter(django_filters.FilterSet):
    class Meta:
        model = Applicant
        fields = ['admNo', 'firstName', 'lastName']
        #exclude = ['IdorBirth', 'guardian']

class BursaryFilter(django_filters.FilterSet):
    class Meta:
        model = Bursary
        fields = ['category']

class InstitutionFilter(django_filters.FilterSet):
    class Meta:
        model = Institution
        fields = ['institutionName', 'institutionLevel']
         