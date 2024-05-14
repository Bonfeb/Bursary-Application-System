from bursary.models import *

applicants = Applicant.objects.all()

firstApplicant = Applicant.objects.first()

lastApplicant = Applicant.objects.last()

applicantByName = Applicant.objects.get(name='Stan')

applicantById = Applicant.objects.get(id=1)

firstApplicant.order_set.all()

applications = Applications.objects.first()
guardianName = applications.Applicant.name

bursary = Bursary.objects.filter(category="Pending")

leastToGreatest = Bursary.objects.all().application_by('id')
greatestToLeast = Bursary.objects.all().application_by('id')

applications = Applicant.application_set.all()
