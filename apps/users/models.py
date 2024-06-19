from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from apps.users.manager import UserManager
from django.utils.text import slugify
import uuid

from apps.core.models import TimestampedModel

from django.utils import timezone

import datetime
import secrets
import random

## AbstructBaseUser has provite some default field ( password, last_login, is_active )
class User(AbstractBaseUser, TimestampedModel, PermissionsMixin):

    class GenderType(models.TextChoices):
        MALE   = 'Male', 'male'
        FEMALE = 'Female', 'female'
        OTHERS  = 'Others', 'others'

    class ReligionType(models.TextChoices):
        ISLAM = 'Islam', 'islam'
        HINDU = 'Hindu ', 'hindu'
        CHRISTIAN = 'Christian', 'christian'
        BUDDHIST  = 'Buddhist', 'buddhist'
        OTHERS = 'Others', 'others'

    class AuthProvider(models.TextChoices):
        LOCAL     = 'Local', 'local'
        GOOGLE    = 'Google', 'google'
        TWITTER   = 'Twitter', 'twitter'
        FACEBOOK  = 'Facebook', 'facebook'
        INSTAGRAM = 'Instagram', 'instagram'

    id        = models.UUIDField( primary_key = True, unique=True, default = uuid.uuid4, editable=False )
    slug      = models.SlugField(unique=True, blank=True, null=True)

    email     = models.EmailField(
                    unique=True,
                    verbose_name="Email address",
                    max_length=255,
                )
    phone     = models.CharField(
                    unique=True,
                    verbose_name="Phone number",
                    max_length=30,
                    null = True,
                    blank=True
                )
    first_name = models.CharField(verbose_name="First name", max_length=255, null=True, blank=True)
    last_name  = models.CharField(verbose_name="Last name", max_length=255, null=True, blank=True)

    gender = models.CharField(
                verbose_name="Gender", 
                max_length=10, 
                choices=GenderType.choices, 
                null=True, blank=True
            )

    religion = models.CharField(
                verbose_name="Religion", 
                max_length=20, 
                choices=ReligionType.choices, 
                null=True, blank=True
            )
    dob      = models.DateField(verbose_name="Date of birth", null=True, blank=True) 

    image    = models.ImageField(upload_to="ProfileImage/", verbose_name="Image", null=True, blank=True)



    ## User Permission and Roll
    is_active   = models.BooleanField(verbose_name="Active", default = True)
    is_admin    = models.BooleanField(verbose_name="Admin", default = False)

    is_email_verified = models.BooleanField(verbose_name="Email Verification", default = False)
    email_verified_at = models.DateTimeField(verbose_name="Email Verification Time", null=True, blank=True)

    is_phone_verified = models.BooleanField(verbose_name="Phone Verification", default = False)
    phone_verified_at = models.DateTimeField(verbose_name="Phone Verification Time", null=True, blank=True)

    is_membership = models.BooleanField(verbose_name="Membership", default = False)

    auth_provider = models.CharField(
        verbose_name = "Authentication With",
        max_length=20, 
        choices=AuthProvider.choices, 
        default=AuthProvider.LOCAL
    )

    fcm_device_token = models.TextField(blank=True, null=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['phone']

    
    def __str__(self):
        return self.email
    
    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        # return True      ## Default
        return self.is_admin

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        # return True      ## Default
        return self.is_admin

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

    @property
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    @property
    def name(self):
        return f"{self.first_name} {self.last_name}"
    
    @property
    def f_name(self):
        if self.first_name:
            return self.first_name
        return None

    @property
    def l_name(self):
        if self.last_name:
            return self.last_name
        return None

    @property
    def age(self):
        if self.dob:
            # today = datetime.date.today()  ## NOTE:- Automatic Handling of Timezones
            today = timezone.now().date()    ## NOTE:- Integration with Django Settings `TIME_ZONE `

            age   = today.year - self.dob.year - ((today.month, today.day) < (self.dob.month, self.dob.day))
            return age
        else:
            return None
        
    def save(self, *args, **kwargs):

        ## NOTE:- Save The Slug 
        if not self.slug:
            # base_slug = slugify(f"{self.first_name}-{self.last_name}-{self.email.split('@')[0]}")
            base_slug = slugify(f"{self.email.split('@')[0]}")
            slug = base_slug
            count = 1
            while User.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{count}"
                count += 1
            self.slug = slug

        ## NOTE:- Save email_verified_at when is_email_verified = True
        if self.is_email_verified and not self.email_verified_at:
            self.email_verified_at = timezone.now()
        

        ## NOTE:- Save phone_verified_at when is_phone_verified = True
        if self.is_phone_verified and not self.phone_verified_at:
            self.phone_verified_at = timezone.now()

        super().save(*args, **kwargs)


    class Meta:
        # db_table = 'users'
        verbose_name = 'User'
        verbose_name_plural = 'Users'





class UserOTP(TimestampedModel):
    user    = models.ForeignKey(User, on_delete=models.CASCADE, related_name="otp")
    otp     = models.IntegerField()
    token   = models.CharField(max_length=100, null=True, blank=True)
    is_used = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.email} - {self.otp}"

    def generate_token(self):
        # generate 64 character token
        token = secrets.token_urlsafe(64)
        return token

    def generate_code(self):
        # generate 6 digit otp
        # otp = int(random() * 1000000)
        otp = random.randint(100000, 999999)
        return str(otp).zfill(6)

    def save(self, *args, **kwargs):
        if not self.otp:
            self.otp = self.generate_code()

        if not self.token:
            self.token = self.generate_token()

        super().save(*args, **kwargs)