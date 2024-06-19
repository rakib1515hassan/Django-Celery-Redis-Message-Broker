from django.core.management.base import BaseCommand
from django.utils import timezone

from apps.users.models import User

class Command(BaseCommand):
    help = 'Setup the project'

    def handle(self, *args, **options):
        user = User()

        user.first_name = "Mr Super"
        user.last_name  = "Admin"
        user.email = "admin@test.com"
        user.phone = "01515612682"

        user.is_superuser = True
        user.is_admin  = True
        user.is_active = True

        # Set email verification fields
        user.is_email_verified = True
        user.email_verified_at = timezone.now()

        # Set phone verification fields
        user.is_phone_verified = True
        user.phone_verified_at = timezone.now()

        user.set_password("admin")
        user.save()

        self.stdout.write(self.style.SUCCESS("Admin user created"))





