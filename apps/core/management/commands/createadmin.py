from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils.text import capfirst
from django.core.management import CommandError
from getpass import getpass
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.core.validators import validate_email

User = get_user_model()

class Command(BaseCommand):
    help = 'Create a superuser with email, phone, and password'

    def handle(self, *args, **options):
        try:
            ## Email Validation
            while True:
                email = input("Email: ")
                if email:
                    try:
                        validate_email(email)
                    except ValidationError:
                        self.stdout.write(self.style.ERROR('Email: Enter a valid email address.'))
                        continue

                    if User.objects.filter(email=email).exists():
                        self.stdout.write(self.style.ERROR('Email: That Email address is already taken.'))
                        continue
                    break
                else:
                    # print("Email is required.")
                    self.stdout.write(self.style.ERROR(f"Email: Email field cannot be blank."))
            


            ## Phone Validation
            while True:
                phone = input("Phone: ")
                if phone:
                    if User.objects.filter(phone=phone).exists():
                        self.stdout.write(self.style.ERROR('Phone: That Phone number is already taken.'))
                        continue
                    if len(phone) > 14 or len(phone) < 11:
                        self.stdout.write(self.style.ERROR('Phone: Enter a valid phone number.'))
                        continue
                    break
                else:
                    # print("Phone is required.")
                    self.stdout.write(self.style.ERROR(f"Phone: Phone field cannot be blank."))



            ## Password and Confirm Password Validation
            while True:
                password = getpass("Password: ")
                if password:
                    if len(password) < 8:
                        self.stdout.write(self.style.ERROR('Password: Password is too small. Please enter a strong password.'))
                        continue
                    break
                else:
                    # print("Password is required.")
                    self.stdout.write(self.style.ERROR(f"Password: Password field cannot be blank."))
            
            while True:
                confirm_password = getpass("Password (again): ")
                if confirm_password:
                    if password != confirm_password:
                        self.stdout.write(self.style.ERROR("Error: The passwords do not match."))
                        continue
                    break
                else:
                    # print("Confirm password is required.")
                    self.stdout.write(self.style.ERROR(f"Password (again): Password (again) field cannot be blank."))



            try:
                self.create_superuser(email, phone, password)
                self.stdout.write(self.style.SUCCESS(f"Superuser created successfully. Email: {email}, Phone: {phone}"))
                # break
            except (ValidationError, ValueError) as e:
                # print('; '.join(e.messages))
                self.stdout.write(self.style.ERROR(f"Error: {str(e)}"))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error: {str(e)}"))
        
        except KeyboardInterrupt:
            self.stdout.write(self.style.ERROR(f"\nOperation cancelled."))


    def stop(self, signum=None, frame=None):
        """Customize the message displayed when the command is interrupted."""
        self.stdout.write(self.style.ERROR("Operation cancelled."))
        super(Command, self).stop(signum, frame)

    def create_superuser(self, email, phone, password):
        User.objects.create_superuser(
            email=email,
            phone=phone,
            password=password
        )
        # self.stdout.write(self.style.SUCCESS(f"Superuser created successfully. Email: {email}, Phone: {phone}"))
