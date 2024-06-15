from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator
from .models import ContentItem, User
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken

# Get the user model
User = get_user_model()

# Serializer for user registration and representation
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,  # Ensure password is write-only
        required=True,  # Password is required
        validators=[
            # Password must meet the specified criteria
            RegexValidator(
                regex=r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[A-Za-z\d]{8,}$',
                message=_("Password must be at least 8 characters long, contain one uppercase letter, one lowercase letter, and one number")
            )
        ]
    )

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'full_name', 'phone', 'address', 'city', 'state', 'country', 'pincode']

    def create(self, validated_data):
        # Create a new user with the validated data
        user = User.objects.create_user(**validated_data)
        return user

# Serializer for content items
class ContentItemSerializer(serializers.ModelSerializer):
    categories = serializers.ListField(
        child=serializers.CharField(max_length=100),
        required=False  # Categories are optional
    )

    class Meta:
        model = ContentItem
        fields = ['id', 'author', 'title', 'body', 'summary', 'categories', 'document', 'created_at', 'updated_at']

    def create(self, validated_data):
        # Pop categories from validated data and join them into a single string
        categories_data = validated_data.pop('categories', [])
        validated_data['categories'] = ','.join(categories_data)
        # Create the content item with the validated data
        content_item = ContentItem.objects.create(**validated_data)
        return content_item

    def update(self, instance, validated_data):
        # Pop categories from validated data and update instance fields
        categories_data = validated_data.pop('categories', [])
        instance.title = validated_data.get('title', instance.title)
        instance.body = validated_data.get('body', instance.body)
        instance.summary = validated_data.get('summary', instance.summary)
        instance.document = validated_data.get('document', instance.document)
        instance.categories = ','.join(categories_data)
        # Save the updated instance
        instance.save()
        return instance

    def to_representation(self, instance):
        # Convert categories string back to list for representation
        representation = super().to_representation(instance)
        representation['categories'] = instance.categories.split(',') if instance.categories else []
        return representation

# Serializer for searching content items
class ContentItemSearchSerializer(serializers.Serializer):
    query = serializers.CharField(required=True, max_length=100)  # Search query is required and has a max length of 100

# Serializer for user login
class LoginSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)  # Password is required with specified length
    email = serializers.CharField(max_length=255, min_length=3)  # Email is required with specified length
    tokens = serializers.SerializerMethodField()  # Field to store tokens

    def get_tokens(self, obj):
        # Retrieve user tokens
        user = User.objects.get(email=obj['email'])
        return {
            'refresh': user.tokens()['refresh'],
            'access': user.tokens()['access']
        }

    class Meta:
        model = User
        fields = ['password', 'email', 'tokens']

    def validate(self, attrs):
        email = attrs.get('email', '')
        password = attrs.get('password', '')

        # Authenticate the user with provided email and password
        user = authenticate(request=self.context.get('request'), email=email, password=password)

        if not user:
            # Raise an error if authentication fails
            raise AuthenticationFailed('Invalid credentials, try again')
        if not user.is_active:
            # Raise an error if the user account is disabled
            raise AuthenticationFailed('Account disabled, contact admin')
        return {
            'email': user.email,
            'username': user.username,
            'tokens': user.tokens
        }
