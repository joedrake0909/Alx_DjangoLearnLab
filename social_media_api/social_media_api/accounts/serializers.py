from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token

User = get_user_model()


class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.
    Handles password hashing and token creation.
    """
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    password_confirm = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'password_confirm', 'bio', 'profile_picture']
        extra_kwargs = {
            'email': {'required': True},
        }
    
    def validate(self, attrs):
        """Validate that passwords match."""
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs
    
    def create(self, validated_data):
        """Create a new user with hashed password and generate token."""
        validated_data.pop('password_confirm')
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            bio=validated_data.get('bio', ''),
            profile_picture=validated_data.get('profile_picture', None)
        )
        # Create token for the user
        Token.objects.create(user=user)
        return user


class UserLoginSerializer(serializers.Serializer):
    """
    Serializer for user login.
    """
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True, style={'input_type': 'password'})


class UserProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for user profile information.
    """
    followers_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'bio', 'profile_picture', 'followers_count', 'following_count', 'date_joined']
        read_only_fields = ['id', 'username', 'date_joined']
    
    def get_followers_count(self, obj):
        """Get the count of followers."""
        return obj.followers.count()
    
    def get_following_count(self, obj):
        """Get the count of users being followed."""
        return obj.following.count()
