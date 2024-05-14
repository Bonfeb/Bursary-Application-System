from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.views.generic import ListView, DetailView
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from .forms import *
from django.forms import inlineformset_factory, formset_factory
from django.contrib import messages
from django.core.mail import send_mail, get_connection
#from django.core.mail.backends.smtp import EmailBackend
from django.contrib.auth import authenticate, login, logout
from .decorators import unauthenticated_user, allowed_users, admin_only
from .filters import * 
from .models import *
from django.utils import timezone
import datetime
from django.conf import settings

from django.template import Context
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, PageTemplate, BaseDocTemplate, PageBreak
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import PageBreak, Spacer, PageTemplate, Paragraph
from reportlab.platypus.doctemplate import PageTemplate, BaseDocTemplate
from reportlab.platypus.frames import Frame
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas
from django.template.loader import get_template

# Create your views here.
def index(request):
    user=request.user

    applicant = Applicant.objects.all()
    bursaries = Bursary.objects.all()
    pending_bursaries = bursaries.filter(status='Pending')
    total_pending_bursaries = bursaries.filter(status='Pending').count()

    current_datetime = timezone.now()
    context = {
        'applicant': applicant,
        'bursaries': bursaries,
        'pending_bursaries': pending_bursaries,
        'total_pending_bursaries': total_pending_bursaries,
        'current_datetime': current_datetime
    }
    print(current_datetime)
    print("pending bursaries", pending_bursaries)
    return render(request, 'index.html', context)

def requirements(request):
    return render(request, 'requirements.html', {'navbar': 'requirements'})

@login_required(login_url='login')
@allowed_users(allowed_roles=['applicant'])
def contact(request):
    user = request.user

    subject = ''
    message = ''
    senderEmail = ''
    if request.method == 'POST':
        subject = request.POST['subject']
        message =request.POST['message']
        senderEmail = user.applicant.email

        try:
            recipientEmail = 'bonfebdevs@example.com' 
            send_mail(
                subject, 
                message,  
                senderEmail,  
                [recipientEmail],
                #fail_silently=False,  # Set to True to suppress exceptions (not recommended for debugging)
            )
            print(subject, message)
            return redirect('applicant_dashboard')
        except:
            return redirect('applicant_dashboard')

    context={
        'message': message,
        'subject': subject,
        'senderEmail': senderEmail
    }
    return render(request, 'contact.html', context)

@unauthenticated_user
def login_user(request):
    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect to a success page.
            return redirect('index')
        else:
             # Return an 'invalid login' error message.
            messages.error(request, "Error Logging in. Check Username or Password...")
            return redirect('login')
    else:
        return render(request, 'user/login.html')

@unauthenticated_user
def register(request):
    form = CustomUserCreationForm()
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')

            applicant = Applicant(user=user)
            applicant.save()

            group, created = Group.objects.get_or_create(name='applicant')
            user.groups.add(group)

            messages.success(request, "Account was Created Successfully! Welcome" + username)
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    context = {
        'form': form
    }
    return render(request, 'user/register.html', context) 

@login_required(login_url='login')
#@allowed_users(allowed_roles=['admin' 'applicant'])
def profile(request):
    user=request.user
    return render(request, 'user/profile.html')

@login_required(login_url='login')
#@allowed_users(allowed_roles=['admin', 'applicant'])
def profile_update(request):
    user=request.user
    if request.method == 'POST':
        userForm = UserProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if userForm.is_valid():
            userForm.save()
            messages.success(request, "Profile Updated Successfully!")
            return redirect('profile')
    else:
        userForm = UserProfileUpdateForm(instance=request.user)
        applicant, created = Applicant.objects.get_or_create(user=request.user)

    context={
        'userForm': userForm
    }
    return render(request, 'user/profile_update.html', context)

@login_required(login_url='login')
@admin_only
def admin_dashboard(request):
    user=request.user
    bursaries = Bursary.objects.all()
    applicants = Applicant.objects.all()
    institution = Institution.objects.all()

    constituencies = Constituency.objects.prefetch_related('ward_set')

    total_applicants = applicants.count()
    total_bursaries = bursaries.count()
    applied_bursaries = Bursary.objects.filter(applicant__isnull=False).distinct()
    disbursed_bursaries = bursaries.filter(status='Fully Disbursed').count()
    pending_bursaries = bursaries.filter(status='Pending').count()
    in_progress = bursaries.filter(status='Disbursement in Progress').count()
    rejected = bursaries.filter(status='Rejected').count()

    bursaryFilter = BursaryFilter(request.GET, queryset=bursaries)
    bursaries = bursaryFilter.qs

    applicantFilter = ApplicantFilter(request.GET, queryset=applicants)
    applicants = applicantFilter.qs

    institutionFilter = InstitutionFilter(request.GET, queryset=institution)
    institution = institutionFilter.qs

    context = {
        'bursaries': bursaries, 
        'applicants': applicants,
        'total_applicants': total_applicants, 
        'total_bursaries': total_bursaries,
        'disbursed_bursaries': disbursed_bursaries, 
        'pending_bursaries': pending_bursaries,
        'in_progress': in_progress, 
        'applied_bursaries':applied_bursaries,
        'bursaryFilter': bursaryFilter,
        'applicantFilter': applicantFilter,
        'institutionFilter': institutionFilter,
        'institution': institution,
        'constituencies': constituencies,
        'rejected': rejected
        }
    return render(request, 'output/admin_dashboard.html', context)

@login_required
class BursaryListView(ListView):
    model = Bursary
    template_name = 'applicant_dashboard.html'
    context_object_name = 'bursaries'

@login_required
class BursaryDetailView(DetailView):
    model = Bursary
    template_name = 'applicant_dashboard.html'
    context_object_name = 'bursary'

@login_required(login_url='login')
@allowed_users(allowed_roles=['applicant'])
def applicant_dashboard(request):
    user = request.user
    applied_bursaries = []
    bursaries = []
    total_bursaries = []
    disbursed_bursaries = []
    disbursed_bursaries = []
    pending_bursaries = []
    in_progress = []
    pendingBursaries = []
    totalAvailableBursaries = []
    rejected = []
    appliedBursaries = []
    try:
        applicant = Applicant.objects.get(user=user)
        bursaries = Bursary.objects.all()
        appliedBursaries = Bursary.objects.filter(applicant=applicant)

        availableBursaries = bursaries.filter(status='Pending')
        totalAvailableBursaries = availableBursaries.count()

        total_bursaries = bursaries.filter(applicant=applicant).count()
        rejected = bursaries.filter(status='Rejected', applicant=applicant).count()
        disbursed_bursaries = bursaries.filter(status='Fully Disbursed', applicant=applicant).count()
        pending_bursaries = bursaries.filter(status='Pending', applicant=applicant).count()
        in_progress = bursaries.filter(status='Disbursement in Progress', applicant=applicant).count()

        total_applied_bursaries = appliedBursaries.count()
        print("Number of bursaries:", bursaries.count())
        for bursary in bursaries:
            print("Bursary details:", bursary)
        for bursaryA in appliedBursaries:
            print("Applied:", bursaryA)
        for bursaryB in availableBursaries:
            print("Available:", bursaryB)
        print(totalAvailableBursaries)

    except Applicant.DoesNotExist:
        rejected = 0
        disbursed_bursaries = 0
        pending_bursaries = 0
        in_progress = 0
        total_applied_bursaries = 0
        total_bursaries = 0
        appliedBursaries = 0
    
    context = {
        'appliedBursaries': appliedBursaries,
        'bursaries': bursaries,  
        'total_bursaries': total_bursaries,
        'total_applied_bursaries': total_applied_bursaries,
        'availableBursaries': availableBursaries,
        'disbursed_bursaries': disbursed_bursaries, 
        'pending_bursaries': pending_bursaries,
        'in_progress':in_progress,
        #'pendingBursaries': pendingBursaries,
        'totalAvailableBursaries': totalAvailableBursaries,
        'rejected': rejected
        }
    return render(request,'output/applicant_dashboard.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['applicant'])
def bursary_application(request, bursary_id):
    bursary = get_object_or_404(Bursary, id=bursary_id)
    applicant = request.user.applicant

    if bursary in applicant.bursary.all():
        messages.error(request, "You have already applied for this bursary.")
        return redirect('applicant_dashboard')

    if not (applicant.constituency == bursary.constituency or applicant.ward == bursary.ward):
        messages.error(request, "You are not eligible to apply, bursary not in your constituency or ward.")
        return redirect('applicant_dashboard')

    if request.method == 'POST':
        applicant.bursary.add(bursary)
        #applicant.save()
        messages.success(request, "Bursary successfully applied!")
        return redirect('applicant_dashboard')  # Redirect to a success page
    context={
        'bursary': bursary
    }
    return render(request, 'application/bursary_application.html', context)

@login_required(login_url='login')
@admin_only
def applicant(request, pk_test):
    applicant = Applicant.objects.get(id=pk_test)
    bursaries = Bursary.objects.filter(applicant=applicant)
    applied_bursaries = Bursary.objects.filter(applicant=applicant)
    applied_bursaries_count = applied_bursaries.count() 

    if not bursaries.exists():
        bursaries = Bursary.objects.none()

    myFilter = BursaryFilter(request.GET, queryset=bursaries)
    #bursaries = myFilter.qs

    context = {
        'applicant': applicant, 
        'bursaries': myFilter.qs, 
        'myFilter':myFilter,
        'applied_bursaries_count': applied_bursaries_count
        }

    return render(request, 'output/applicant.html', context)

@login_required(login_url='login')
@admin_only
def applicant_list(request):
    applicants = Applicant.objects.all()

    applicantFilter = ApplicantFilter(request.GET, queryset=applicants)
    applicants = applicantFilter.qs

    context={
        'applicants': applicants,
        'applicantFilter': applicantFilter
    }
    return render(request, 'output/applicant_list.html', context)

@login_required(login_url='login')
@admin_only
def institution_list(request):
    institution = Institution.objects.all()

    institutionFilter = InstitutionFilter(request.GET, queryset=institution)
    institution = institutionFilter.qs
    
    context={
        'institution': institution,
        'institutionFilter': institutionFilter
    }
    return render(request, 'output/institution_list.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['applicant'])
def applicant_filling_details(request):
    #applicant=request.user.applicant
    if request.method == 'POST':
        form = FillingDetailsForm(request.POST, request.FILES)
        if form.is_valid():
            firstName = form.cleaned_data['firstName']
            middleName = form.cleaned_data['middleName']
            lastName = form.cleaned_data['lastName']
            gender = form.cleaned_data['gender']
            email = form.cleaned_data['email']
            contact = form.cleaned_data['contact']
            DOB = form.cleaned_data['DOB']
            IdOrBirth = form.cleaned_data['IdOrBirth']
            studyLevel = form.cleaned_data['studyLevel']
            admNo = form.cleaned_data['admNo']
            studyYear = form.cleaned_data['studyYear']
            course = form.cleaned_data['course']
            institutionName = form.cleaned_data['institutionName']
            constituencyName = form.cleaned_data['constituencyName']
            wardName = form.cleaned_data['wardName']

            guardianName = form.cleaned_data['guardianName']
            guardianContact = form.cleaned_data['guardianContact']
            guardianID = form.cleaned_data['guardianID']
            guardianGender = form.cleaned_data['guardianGender']
            guardianOccupation = form.cleaned_data['guardianOccupation']

            guardian = Guardian(guardianName=guardianName, guardianContact=guardianContact, guardianID=guardianID, guardianGender=guardianGender, guardianOccupation=guardianOccupation)
            guardian.save()

            applicant = Applicant(user=request.user, firstName=firstName, middleName=middleName, lastName=lastName, gender=gender, email=email, contact=contact, DOB=DOB, IdOrBirth=IdOrBirth, studyLevel=studyLevel, admNo=admNo, studyYear=studyYear, course=course, institution=institutionName, constituency=constituencyName, ward=wardName, guardian=guardian)
            applicant.save()

            if applicant.guardian:
                applicant.guardian.guardianName = guardianName
                applicant.guardian.guardianContact = guardianContact
                applicant.guardian.guardianID = guardianID
                applicant.guardian.guardianGender = guardianGender
                applicant.guardian.guardianOccupation = guardianOccupation
                applicant.guardian.save()
            else:
                # Create a new Guardian instance
                new_guardian = Guardian(guardianName=guardianName, guardianContact=guardianContact, guardianID=guardianID, guardianGender=guardianGender, guardianOccupation=guardianOccupation)
                new_guardian.save()

                # Associate the new Guardian with the Applicant
                applicant.guardian = new_guardian
                applicant.save()
            #guardian.save()

            #applicant.guardian = guardian
            #applicant.save()

            return redirect('applicant_dashboard')
        else:
            messages.error(request, "Error with the forms! Try Again") 
            return redirect('filling_details')          
    else:
        form = FillingDetailsForm()
    context={
        'form': form
    }
    return render(request, 'application/filling_details.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['applicant'])
def applicant_updateDetails(request):
    applicant = request.user.applicant
    guardian = applicant.guardian
    
    applicantUpdateForm = UpdateDetailsForm(instance=applicant)
    guardianUpdateForm = UpdateGuardianForm(instance=guardian)
    if request.method == 'POST':
        applicantUpdateForm = UpdateDetailsForm(request.POST, request.FILES, instance=applicant)
        guardianUpdateForm = GuardianForm(request.POST, request.FILES, instance=guardian)

        if applicantUpdateForm.is_valid() and guardianUpdateForm.is_valid():
            # Update the Guardian model
            guardianUpdateForm.save()

            # Update the guardian field in the Applicant model
            updatedGuardian = guardianUpdateForm.save(commit=False)
            updatedGuardian.save()

            applicant.guardian = updatedGuardian
            applicant.save()

            return redirect('applicant_dashboard')
        else:
            messages.error(request, "Error with the forms! Try Again")
    else:
        applicantUpdateForm = UpdateDetailsForm(instance=applicant)
        guardianUpdateForm = UpdateGuardianForm(instance=guardian)

    context = {
        'applicantUpdateForm': applicantUpdateForm,
        'guardianUpdateForm': guardianUpdateForm
    }
    return render(request, 'application/update_details.html', context)

@login_required(login_url='login')
@admin_only
def add_bursary(request):
    user=request.user
    if request.method == 'POST':
        form = AddBursaryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Bursary Created Successfully!")
            return redirect('admin_dashboard')
        else:
            #return redirect('add_bursary')
            print("form error")
    else:
        form = AddBursaryForm()
    context = {
        'form': form
    }
    return render(request, 'admin/add_bursary.html', context)

@login_required(login_url='login')
@admin_only
def update_bursary(request, bursary_id):
    
    bursary = Bursary.objects.get(id=bursary_id)
    form = UpdateBursaryForm(instance=bursary)
    if request.method == 'POST':
        form = UpdateBursaryForm(request.POST, instance=bursary)
        if form.is_valid():
            form.save()
            messages.success(request, "Bursary Updated Successfully!")
            return redirect('admin_dashboard')
    else:
        form = UpdateBursaryForm(instance=bursary)
    context = {
        'form': form,
        'bursary': bursary
    }
    return render(request, 'admin/update_bursary.html', context)

@login_required(login_url='login')
@admin_only
def delete_bursary(request, bursary_id):
    user=request.user
    bursary = Bursary.objects.get(id=bursary_id)
    #bursary = Bursary.objects.get(id=bursary_id)
    if request.method == "POST":
        bursary.delete()
        messages.success(request, "Bursary Successfully Deleted!")
        if request.user.groups.filter(name='admin').exists():
            return redirect('admin_dashboard')
        elif request.user.groups.filter(name='applicant').exists():
            return redirect('applicant_dashboard')
    context = {
        'item':bursary
        }
    if request.user.groups.filter(name='admin').exists():
        return render(request, 'admin/delete_bursary.html', context)
    elif request.user.groups.filter(name='applicant').exists():
        return render(request, 'application/applicant_delete_bursary_application.html', context)

@login_required(login_url='login')
@admin_only
def generate_pdf(request):
    applicantDisbursed = Applicant.objects.filter(bursary__status='Disbursed')
    
    if not applicantDisbursed.exists():
        return HttpResponse("No Disbursed applicants found.", content_type='text/plain', status=404)

    # Response object with a PDF content type
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="Disbursed Applicants.pdf"'

    #PDF template with a footer, title, and logo
    class CustomPageTemplate(PageTemplate):
        def __init__(self, id, pagesize):
            PageTemplate.__init__(self, id, pagesize)
            self.title = "Disbursed Applicants"
            self.logo_path = "static/images/Image1.jpg" 
        def beforeDrawPage(self, canvas, doc):
            canvas.saveState()
            canvas.setFont("Helvetica-Bold", 16)
            canvas.drawString(inch, doc.height - inch, self.title)
            canvas.drawImage(self.logo_path, doc.width / 3, doc.height - inch - 0.25 * inch, width=1.5*inch, height=1.5*inch)
            canvas.restoreState()

    custom_page = Frame(x1=30, y1=30, width=750, height=550, showBoundary=1)
    page_template = PageTemplate(id='custom_template', frames=[custom_page], pagesize=landscape(letter))
    #PDF document using the custom template
    doc = SimpleDocTemplate(response, pagesize=landscape(letter), rightMargin=30, leftMargin=30, topMargin=60, bottomMargin=30)
    doc.addPageTemplates(
        (page_template))

    #PDF table data
    data = [["Applicant Name", "Study Level", "Guardian", "Ward"]]
    for applicant in applicantDisbursed:
        data.append([
            f"{applicant.firstName} {applicant.lastName}",
            applicant.studyLevel,
            applicant.guardian.guardianName if applicant.guardian else "No Guardian",
            applicant.ward,
        ])

    #Table with the data
    table = Table(data)
    table.setStyle(
        TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ])
        )

    #Adding the table to the PDF document
    elements = [table, PageBreak()]

    #Adding the print date, sign, and stamp at the end
    print_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    sign = ""
    stamp = ""

    elements.extend([
        Paragraph(f"Print Date: {print_date}", getSampleStyleSheet()['Normal']),
        Spacer(2, 12),
        Paragraph(f"Sign: {sign}", getSampleStyleSheet()['Normal']),
        Spacer(2, 12),
        Paragraph(f"Stamp: {stamp}", getSampleStyleSheet()['Normal']),
    ])

    doc.build(elements)

    return response

@login_required(login_url='login')
@admin_only
def update_institutionContact(request, institution_id):
    institution = Institution.objects.get(id=institution_id)
    form = InstitutionContactForm(instance=institution)
    if request.method == 'POST':
        form = InstitutionContactForm(request.POST, instance=institution)
        if form.is_valid():
            form.save()
            messages.success(request, "Institution Contact details updated successfully!")
            return redirect('admin_dashboard')
        else:
            form = InstitutionContactForm(instance=institution)
    context={
        'form': form,
        'institution': institution
    }
    return render(request, 'admin/update_institutionContact.html', context)

@login_required(login_url='login')
@admin_only
def institution_applicants(request, institution_id):
    # Get the institution based on the institution_id
    institution = Institution.objects.get(id=institution_id)

    # Get the list of applicants associated with the institution
    applicants = Applicant.objects.filter(institution=institution)

    context={
        'applicants': applicants,
        'institution_id': institution.id,
        'institution': institution
    }
    if request.GET.get('pdf'):
        # Generate a PDF response
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{institution.institutionName} Applicants.pdf"'
        
        table_frame = Frame(x1=30, y1=30, width=750, height=350, showBoundary=0)
        footer_frame = Frame(x1=30, y1=10, width=750, height=20, showBoundary=0)
        #PDF template with a footer, title, and logo
        class CustomPageTemplate(PageTemplate):
            def __init__(self, id, pagesize):
                PageTemplate.__init__(self, id, pagesize)
                self.title = f'"{institution.institutionName} Applicants List"'
                self.logo_path = "static/images/KC-logo.svg" 

                table_height = 350  
                footer_height = 20

                self.frames.extend([
                Frame(30, 30, 750, table_height, id='table_frame', showBoundary=1),
                Frame(30, 10, 750, footer_height, id='footer_frame', showBoundary=0)
                ])

            def beforeDrawPage(self, canvas, doc):
                canvas.saveState()
                canvas.setFont("Helvetica-Bold", 16)
                canvas.drawString(inch, doc.height - inch, self.title)
                canvas.drawImage(self.logo_path, doc.width / 3, doc.height - inch - 0.25 * inch, width=1.5*inch, height=1.5*inch)
                canvas.restoreState()

        custom_page = Frame(x1=30, y1=30, width=750, height=550, showBoundary=1)
        page_template = PageTemplate(id='custom_template', frames=[custom_page], pagesize=landscape(letter))

        #PDF document using the custom template
        doc = SimpleDocTemplate(response, pagesize=landscape(letter), rightMargin=30, leftMargin=30, topMargin=60, bottomMargin=30)
        doc.addPageTemplates(
            (page_template))

        #PDF table data
        data = [["First Name", "Last Name", "Current Year/Form", "Admission Number"]]
        #looping institution's applicants:
        for applicant in applicants:
            data.append([
                f"{applicant.firstName}",
                applicant.lastName,
                applicant.studyYear,
                applicant.admNo,
            ])

        #Table with the data
        table = Table(data)
        table.setStyle(
            TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 0, colors.black)
            ])
            )

        #Adding the table to the PDF document
        elements = [table]

        #Adding the print date, sign, and stamp at the end
        print_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        sign = ""
        stamp = ""

        elements.extend([
            Paragraph(f"Print Date: {print_date}", getSampleStyleSheet()['Normal']),
            Spacer(2, 12),
            Paragraph(f"Sign: {sign}", getSampleStyleSheet()['Normal']),
            Spacer(2, 12),
            Paragraph(f"Stamp: {stamp}", getSampleStyleSheet()['Normal']),
        ])

        doc.build(elements)

        return response
    else:
    # Render a template with the list of applicants
        return render(request, 'admin/institution_applicants.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['applicant'])
def applicant_edit_bursary_application(request, bursary_id):
    #user = CustomUser.objects.get(username=request.user.username)
    user=request.user

    bursary = Bursary.objects.get(id=bursary_id)
    bursaryform = EditBursaryApplicationForm(request.POST, instance=bursary)
    applicantForm = ApplicantForm(request.POST, instance=applicant)
    institutionForm = InstitutionForm(request.POST, instance=institution)
    guardianForm = GuardianForm(request.POST, instance=guardian)
    if request.method == 'POST':
        bursaryform = EditBursaryApplicationForm(request.POST, instance=bursary)
        if bursaryForm.is_valid():
            bursaryForm.save()
            messages.success(request, "Bursary Updated Successfully!")
            return redirect('applicant_dashboard')
    else:
        bursaryForm = EditBursaryApplicationForm()
        applicantForm = ApplicantForm()
        institutionForm = InstitutionForm()
        guardianForm = GuardianForm()

    context = {
        'bursaryform': bursaryform,
        'applicantForm': applicantForm,
        'institutionForm': institutionForm,
        'guardianForm': guardianForm
    }
    return render(request, 'application/applicant_edit_bursary.html')

@login_required(login_url='login')
@allowed_users(allowed_roles=['applicant'])
def applicantDelete_bursaryApplication(request, bursary_id):
    #user = CustomUser.objects.get(username=request.user.username)
    user=request.user

    bursary = Bursary.objects.get(id=bursary_id)
    if request.method == "POST":
        bursary.delete()
        messages.success(request, "Bursary Successfully Deleted!")
        return redirect('applicant_dashboard')
    context = {
        'item':bursary
        }
    return render(request, 'application/applicant_delete_bursary_application.html', context)
