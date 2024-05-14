from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.dispatch import receiver

from .models import Applicant

def applicant_profile(sender, instance, created, **kwargs):
    if created:
        group = Group.objects.get(name='applicant')
        instance.groups.add(group)

        Applicant.objects.create(
            user = instance,
            #name = instance.username
        )
        print('Profile Created')

post_save.connect(applicant_profile, sender=User)

@receiver(post_save, sender=User)
def create_applicant_profile(sender, instance, created, **kwargs):
    if created and not instance.is_staff and not instance.is_superuser:
        Applicant.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_applicant_profile(sender, instance, created, **kwargs):
    if created and not instance.is_staff:
        applicant, created = Applicant.objects.get_or_create(user=instance)
        if created:
            applicant.save()
