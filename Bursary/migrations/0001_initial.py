# Generated by Django 5.0.3 on 2025-06-04 16:47

import django.contrib.auth.models
import django.contrib.auth.validators
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Constituency',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('constituencyName', models.CharField(max_length=200, null=True)),
            ],
            options={
                'verbose_name_plural': 'Constituency',
            },
        ),
        migrations.CreateModel(
            name='Guardian',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('guardianName', models.CharField(max_length=100, null=True)),
                ('guardianContact', models.CharField(max_length=25, null=True)),
                ('guardianID', models.FileField(null=True, upload_to='GuardianIDs')),
                ('guardianGender', models.CharField(choices=[('Male', 'Male'), ('Female', 'Female')], max_length=20, null=True)),
                ('guardianOccupation', models.CharField(max_length=200, null=True)),
            ],
            options={
                'verbose_name_plural': 'Guardian',
            },
        ),
        migrations.CreateModel(
            name='Institution',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('institutionName', models.CharField(max_length=200, null=True)),
                ('institutionLevel', models.CharField(choices=[('University', 'University'), ('College', 'College'), ('Secondary', 'Secondary')], max_length=200, null=True)),
                ('institutionStatus', models.CharField(choices=[('Public', 'Public'), ('Private', 'Private')], max_length=200, null=True)),
                ('institutionContact', models.CharField(max_length=35, null=True)),
            ],
            options={
                'verbose_name_plural': 'Institution',
            },
        ),
        migrations.CreateModel(
            name='Ward',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('wardName', models.CharField(max_length=200, null=True)),
                ('constituency', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Bursary.constituency')),
            ],
            options={
                'verbose_name_plural': 'Ward',
            },
        ),
        migrations.CreateModel(
            name='Bursary',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(choices=[('County', 'County'), ('Constituency', 'Constituency'), ('Ward', 'Ward')], max_length=200, null=True)),
                ('bursaryAmount', models.CharField(choices=[('5000', '5000'), ('8000', '8000'), ('10000', '10000'), ('12500', '12500')], max_length=30, null=True)),
                ('financialyear', models.CharField(max_length=200, null=True)),
                ('batchNumber', models.CharField(max_length=200, null=True)),
                ('status', models.CharField(choices=[('Pending', 'Pending'), ('Disbursement in Progress', 'Disbursement in Progress'), ('Fully Disbursed', 'Fully Disbursed'), ('Rejected', 'Rejected')], default='Pending', max_length=200, null=True)),
                ('dateCreated', models.CharField(max_length=200, null=True)),
                ('deadline', models.CharField(max_length=200, null=True)),
                ('constituency', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Bursary.constituency')),
                ('ward', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Bursary.ward')),
            ],
            options={
                'verbose_name_plural': 'Bursary',
            },
        ),
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('profileContact', models.IntegerField(null=True)),
                ('profilePicture', models.ImageField(blank=True, default='images/profile_avatar.jpg', null=True, upload_to='Profile_Images')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Applicant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstName', models.CharField(max_length=30, null=True)),
                ('middleName', models.CharField(max_length=30, null=True)),
                ('lastName', models.CharField(max_length=30, null=True)),
                ('gender', models.CharField(choices=[('Male', 'Male'), ('Female', 'Female')], max_length=20, null=True)),
                ('email', models.EmailField(max_length=200, null=True)),
                ('contact', models.IntegerField(null=True)),
                ('DOB', models.CharField(max_length=200, null=True)),
                ('IdOrBirth', models.FileField(upload_to='IdOrBirths')),
                ('studyLevel', models.CharField(choices=[('University', 'University'), ('College', 'College'), ('Secondary', 'Secondary')], max_length=20, null=True)),
                ('admNo', models.CharField(max_length=20, null=True)),
                ('studyYear', models.CharField(max_length=200, null=True)),
                ('course', models.CharField(max_length=200, null=True)),
                ('bursary', models.ManyToManyField(blank=True, to='Bursary.bursary')),
                ('constituency', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Bursary.constituency')),
                ('guardian', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Bursary.guardian')),
                ('institution', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Bursary.institution')),
                ('ward', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Bursary.ward')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Applicant',
            },
        ),
    ]
