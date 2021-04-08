from django.db import models
from uuid import uuid4


class UserRegisteration(models.Model):
    """
        Creating User Registeration Model
    """

    ROLE_CHOICES = (
        ('Admin', 'Admin'),
        ('Manager', 'Manager'),
    )
    DoesNotExist = None
    object = None

    id = models.UUIDField(default=uuid4, primary_key=True, null=False)
    first_name = models.CharField(verbose_name="First Name", max_length=255, null=False)
    last_name = models.CharField(verbose_name="Last Name", max_length=255, null=True)
    username = models.CharField(verbose_name="Username", max_length=100, null=False, unique=True)
    email_id = models.EmailField(verbose_name="Email Id", max_length=255, null=False, unique=True)
    role = models.CharField(verbose_name="Role",max_length=100, choices=ROLE_CHOICES, null=False)
    mobile_no = models.IntegerField(verbose_name="Mobile Number", unique=True, null=False)
    password = models.CharField(verbose_name="Password", max_length=12, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.email_id
