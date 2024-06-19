from django.db import models
from django.contrib.auth.models import AbstractUser
#from django.utils import timezone

# Create your models here.

class CustomUser(AbstractUser):
    profileContact = models.IntegerField(null=True)
    profilePicture = models.ImageField(default="images/profile_avatar.jpg", upload_to='Profile_Images', blank=True, null=True)
    def __str__(self):
        return f'{self.username}'

class Bursary(models.Model):
    STATUS = (
        ('Pending', 'Pending'),
        ('Disbursement in Progress', 'Disbursement in Progress'),
        ('Fully Disbursed', 'Fully Disbursed'),
        ('Rejected', 'Rejected'),
    )
    CATEGORY = (
        ('County', 'County'),
        ('Constituency', 'Constituency'),
        ('Ward', 'Ward'),
    )
    Amount = (
        ('5000', '5000'),
        ('8000', '8000'),
        ('10000', '10000'),
        ('12500', '12500'),
    )
    category = models.CharField(max_length=200, null=True, choices=CATEGORY)
    bursaryAmount = models.CharField(choices=Amount, max_length=30, null=True)
    financialyear = models.CharField(max_length=200, null=True)
    batchNumber = models.CharField(max_length=200, null=True)
    status = models.CharField(max_length=200, null=True, choices=STATUS, default='Pending')
    dateCreated = models.CharField(max_length=200, null=True)
    deadline = models.CharField(max_length=200, null=True)

    ward = models.ForeignKey('Ward', on_delete=models.CASCADE, null=True, blank=True)
    constituency = models.ForeignKey('Constituency', on_delete=models.CASCADE, null=True, blank=True)
    #wardConstituencyName = models.ForeignKey('Bursary.Ward', 'Bursary.Constituency', on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name_plural = 'Bursary'
    
    def save(self, *args, **kwargs):
        if not self.status:
            self.status = 'Pending'
        super(Bursary, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.category} - {self.ward if self.ward else self.constituency} {self.bursaryAmount} {self.status}'

class Institution(models.Model):
    LEVEL = (
        ('University', 'University'),
        ('College', 'College'),
        ('Secondary', 'Secondary'),
    )
    STATUS = (
        ('Public', 'Public'),
        ('Private', 'Private'),
    )
    institutionName = models.CharField(max_length=200, null=True)
    institutionLevel = models.CharField(null=True, choices = LEVEL, max_length=200)
    institutionStatus = models.CharField(max_length=200, null=True, choices = STATUS)
    institutionContact = models.CharField(max_length=35, null=True)

    class Meta:
        verbose_name_plural = 'Institution'

    def __str__(self):
        return f'{self.institutionName}'

class Constituency(models.Model):
    constituencyName = models.CharField(max_length=200, null=True)

    class Meta:
        verbose_name_plural = 'Constituency'
    
    def __str__(self):
        return self.constituencyName

class Ward(models.Model):
    constituency = models.ForeignKey(Constituency, null=True, on_delete=models.CASCADE)
    wardName = models.CharField(max_length=200, null=True)

    class Meta:
        verbose_name_plural = 'Ward'
    
    def __str__(self):
        return self.wardName

class Guardian(models.Model):
    GENDER = (
        ('Male', 'Male'),
        ('Female', 'Female'),
    )
    guardianName = models.CharField(max_length=100, null=True)
    guardianContact = models.CharField(max_length=25, null=True)
    guardianID = models.FileField(null=True, upload_to='GuardianIDs')
    guardianGender = models.CharField(max_length=20, choices = GENDER, null=True)
    guardianOccupation = models.CharField(max_length=200, null=True)

    class Meta:
        verbose_name_plural = 'Guardian'
    def __str__(self):
        return f'{self.guardianName} - {self.guardianOccupation}'

class Applicant(models.Model):
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
    institution = models.ForeignKey(Institution, null=True, on_delete=models.CASCADE)
    constituency = models.ForeignKey(Constituency, null=True, on_delete=models.CASCADE)
    ward = models.ForeignKey(Ward, null=True, on_delete=models.CASCADE)
    bursary = models.ManyToManyField(Bursary, blank=True)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    firstName = models.CharField(max_length=30, null=True)
    middleName = models.CharField(max_length=30, null=True)
    lastName = models.CharField(max_length=30, null=True)
    gender = models.CharField(max_length=20, choices = GENDER, null=True)
    email = models.EmailField(max_length=200, null=True)
    contact = models.IntegerField(null=True)
    DOB = models.CharField(max_length=200, null=True)
    IdOrBirth = models.FileField(upload_to='IdOrBirths')
    guardian = models.ForeignKey(Guardian, null=True, on_delete=models.CASCADE)
    studyLevel = models.CharField(max_length=20, null=True, choices = LEVEL)
    admNo = models.CharField(max_length=20, null=True)
    studyYear = models.CharField(max_length=200, null=True)
    course = models.CharField(max_length=200, null=True)

    class Meta:
        verbose_name_plural = 'Applicant'

    def __str__(self):
        return f'{self.firstName}  {self.lastName}'