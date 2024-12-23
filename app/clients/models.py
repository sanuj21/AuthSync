from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
import uuid

class API_PLANS(models.TextChoices):
    FREE = 'FREE', 'Free'
    BASIC = 'BASIC', 'Basic'
    PREMIUM = 'PREMIUM', 'Premium'

class ClientApp(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    api_key = models.CharField(max_length=255, unique=True)
    api_key_expires = models.DateTimeField()
    plan = models.CharField(max_length=10, choices=API_PLANS.choices, default=API_PLANS.FREE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class LOGIN_TYPE(models.TextChoices):
    Email = 'Email', 'Email'
    GOOGLE = 'GOOGLE', 'Google'
    GITHUB = 'GITHUB', 'Github'


class ClientUserManager(BaseUserManager):
    """Manager for ClientUser"""

    def create_user(self, email, password=None, **extra_field):
        """Create, save and return a new user"""

        if not email:
            raise ValueError('User must have Email Address.')

        user = self.model(email=self.normalize_email(email), **extra_field)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Create and return superuser"""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user



class ClientUser(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # User details
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=255, null=True, blank=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    password = models.CharField(max_length=255, null=True, blank=True)  # Nullable for non-local logins
    avatar = models.URLField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    # Auth details
    login_type = models.CharField(max_length=10, choices=LOGIN_TYPE.choices, default=LOGIN_TYPE.Email)
    reset_token = models.CharField(max_length=64, null=True, blank=True)
    reset_token_expiry = models.DateTimeField(null=True, blank=True)
    email_verified = models.BooleanField(default=False)
    email_verification_token = models.CharField(max_length=255, null=True, blank=True)

    # Foreign key to reference ClientApp
    client_app = models.ForeignKey('ClientApp', related_name='users', on_delete=models.CASCADE)
    objects = ClientUserManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email



class PAYMENT_STATUS(models.TextChoices):
    PENDING = 'PENDING', 'Pending'
    COMPLETED = 'COMPLETED', 'Completed'
    FAILED = 'FAILED', 'Failed'

class Payment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    amount = models.FloatField()
    currency = models.CharField(max_length=10)
    status = models.CharField(max_length=10, choices=PAYMENT_STATUS.choices, default=PAYMENT_STATUS.PENDING)

    # Payment provider details
    provider = models.CharField(max_length=50)  # e.g., "razorpay", "stripe", "paypal"
    provider_order_id = models.CharField(max_length=255, null=True, blank=True)
    provider_payment_id = models.CharField(max_length=255, null=True, blank=True)
    provider_signature = models.CharField(max_length=255, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    # Foreign key to reference ClientApp
    client_app = models.ForeignKey('ClientApp', related_name='payments', on_delete=models.CASCADE)

    def __str__(self):
        return f"Payment for {self.client_app.name} - {self.amount} {self.currency}"
