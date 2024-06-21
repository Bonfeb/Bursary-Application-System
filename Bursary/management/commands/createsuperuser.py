from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
import os

class Command(BaseCommand):
    help = 'Create a superuser if it does not exist'

    def handle(self, *args, **kwargs):
        if not User.objects.filter(username=os.environ['SUPERUSER_USERNAME']).exists():
            User.objects.create_superuser(
                os.environ['SUPERUSER_USERNAME'],
                os.environ['SUPERUSER_EMAIL'],
                os.environ['SUPERUSER_PASSWORD']
            )
            self.stdout.write(self.style.SUCCESS('Superuser created successfully'))
            print("Super user:", SUPERUSER_USERNAME)
        else:
            self.stdout.write(self.style.WARNING('Superuser already exists'))


