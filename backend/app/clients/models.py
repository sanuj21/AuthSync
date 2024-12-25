from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
import uuid

class PAYMENT_STATUS(models.TextChoices):
    PENDING = 'PENDING', 'Pending'
    COMPLETED = 'COMPLETED', 'Completed'
    FAILED = 'FAILED', 'Failed'

class LOGIN_TYPE(models.TextChoices):
    Email = 'Email', 'Email'
    GOOGLE = 'GOOGLE', 'Google'
    GITHUB = 'GITHUB', 'Github'

class ROLE(models.TextChoices):
    ADMIN = 'ADMIN', 'Admin'
    USER = 'USER ', 'User'



class ApiPlan(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)

    price = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10, default='INR')
    max_requests_per_day = models.IntegerField()
    max_users = models.IntegerField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class ClientApp(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    no_of_users = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    # Foreign key to reference User of Main App
    owner = models.ForeignKey('core.User', related_name='client_apps', on_delete=models.CASCADE, null=True, blank=True)


    def __str__(self):
        return self.name

class Subscription(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField()
    is_active = models.BooleanField(default=True)

    client_app = models.ForeignKey('ClientApp', related_name='subscriptions', on_delete=models.CASCADE)
    plan = models.ForeignKey('ApiPlan', related_name='subscriptions', on_delete=models.CASCADE)

    # API details
    api_key = models.CharField(max_length=255, unique=True, blank=True, null=True)
    api_key_expires = models.DateTimeField(null=True, blank=True)


    def __str__(self):
        return f"{self.client_app.name} - {self.start_date} to {self.end_date}"



class ClientUser(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # User details
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=255, null=True, blank=True)
    name = models.CharField(max_length=255)
    password = models.CharField(max_length=255, null=True, blank=True)  # Nullable for non-local logins
    avatar = models.URLField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    role = models.CharField(max_length=10, choices=ROLE.choices, default=ROLE.USER)

    # Auth details
    login_type = models.CharField(max_length=10, choices=LOGIN_TYPE.choices, default=LOGIN_TYPE.Email)
    reset_token = models.CharField(max_length=64, null=True, blank=True, unique=True)
    reset_token_expiry = models.DateTimeField(null=True, blank=True)
    email_verified = models.BooleanField(default=False)
    email_verification_token = models.CharField(max_length=255, null=True, blank=True, unique=True)

    # Foreign key to reference ClientApp
    client_app = models.ForeignKey('ClientApp', related_name='users', on_delete=models.CASCADE, null=True, blank=True)

    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email



class Payment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    amount = models.FloatField()
    currency = models.CharField(max_length=10, default='INR')
    status = models.CharField(max_length=10, choices=PAYMENT_STATUS.choices, default=PAYMENT_STATUS.PENDING)
    order_id = models.CharField(max_length=255, null=True, blank=True)

    # Payment provider details
    provider = models.CharField(max_length=50)  # e.g., "razorpay", "stripe", "paypal"
    provider_order_id = models.CharField(max_length=255, null=True, blank=True)
    provider_payment_id = models.CharField(max_length=255, null=True, blank=True)
    provider_signature = models.CharField(max_length=255, null=True, blank=True)

    subscription = models.ForeignKey('Subscription', related_name='payments', on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Payment for {self.client_app.name} - {self.amount} {self.currency}"


# Custom fields for ClientUser
class ClientUserCustomField(models.Model):
    user = models.ForeignKey('ClientUser', related_name='custom_fields', on_delete=models.CASCADE)
    key = models.CharField(max_length=255)
    value = models.TextField()

    def __str__(self):
        return f"{self.key}: {self.value}"
