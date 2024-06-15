from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator
from rest_framework_simplejwt.tokens import RefreshToken


class User(AbstractUser):
    USER_ROLES = (
        ('Admin', 'Admin'),
        ('Author', 'Author'),
    )
    
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=60, default="First Last")
    phone = models.CharField(
        max_length=10, 
        validators=[
            RegexValidator(
                regex=r'^\d{10}$', 
                message="Phone number must be 10 digits"
            )
        ]
    )
    address = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=30, blank=True)
    state = models.CharField(max_length=30, blank=True)
    country = models.CharField(max_length=30, blank=True)
    user_role = models.CharField(max_length=10, choices=USER_ROLES, default='Author')
    pincode = models.CharField(
        max_length=6, 
        validators=[
            RegexValidator(
                regex=r'^\d{6}$', 
                message="Pincode must be 6 digits"
            )
        ]
    )
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='cms_app_user_groups',  # Avoid reverse accessor clash
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_query_name='user',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='cms_app_user_permissions',  # Avoid reverse accessor clash
        blank=True,
        help_text='Specific permissions for this user.',
        related_query_name='user',
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'full_name']
    
    def __str__(self):
        return self.email

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }

    # @property
    # def is_staff(self):
    #     return self.is_admin

    class Meta:
        db_table = 'user'


class ContentItem(models.Model):
    title = models.CharField(max_length=30)
    body = models.TextField(max_length=300)
    summary = models.CharField(max_length=60)
    categories = models.CharField(max_length=255, blank=True)  # Ensure max_length is defined
    document = models.FileField(upload_to='documents/')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'content_item'
