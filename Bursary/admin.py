from django.contrib import admin
from .models import *


admin.site_header = 'KCBAWS Admin Dashboard'

#class ApplicantAdmin(admin.ModelAdmin):
    #list_display = ('firstName', 'lastName')

#class FinancialYearAdmin(admin.ModelAdmin):
    #list_display = ('endYear')

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Applicant)
admin.site.register(Institution)
admin.site.register(Constituency)
admin.site.register(Ward)
admin.site.register(Bursary)

class BursaryAdmin(admin.ModelAdmin):
    list_display = ('batchNumber', 'category', 'financialyear')
    list_filter = ('batchNumber',)
    search_fields = ('batchNumber', 'financialyear')

admin.site.register(Guardian)

