from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User, BackgroundCheck


class UserSerializer(serializers.ModelSerializer):
    """User serializer"""
    full_name = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name', 'full_name',
            'user_type', 'phone_number', 'address', 'date_of_birth', 
            'profile_picture', 'is_verified', 'date_joined', 'last_login'
        ]
        read_only_fields = ['id', 'date_joined', 'last_login']
    
    def get_full_name(self, obj):
        return obj.get_full_name()


class UserRegistrationSerializer(serializers.ModelSerializer):
    """User registration serializer"""
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = [
            'username', 'email', 'first_name', 'last_name', 'password', 
            'password_confirm', 'user_type', 'phone_number', 'address', 
            'date_of_birth', 'profile_picture'
        ]
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("Passwords don't match")
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')
        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        return user


class UserLoginSerializer(serializers.Serializer):
    """User login serializer"""
    username = serializers.CharField()
    password = serializers.CharField()
    
    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        
        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise serializers.ValidationError('Invalid credentials')
            if not user.is_active:
                raise serializers.ValidationError('User account is disabled')
            attrs['user'] = user
            return attrs
        else:
            raise serializers.ValidationError('Must include username and password')


class BackgroundCheckSerializer(serializers.ModelSerializer):
    """Background check serializer"""
    user_name = serializers.SerializerMethodField()
    
    class Meta:
        model = BackgroundCheck
        fields = [
            'id', 'user', 'user_name', 'check_type', 'status', 
            'verification_agency', 'reference_number', 'conducted_date', 
            'expiry_date', 'notes', 'documents', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_user_name(self, obj):
        return obj.user.get_full_name()


class UserProfileSerializer(serializers.ModelSerializer):
    """User profile serializer for updates"""
    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'email', 'phone_number', 
            'address', 'date_of_birth', 'profile_picture'
        ]
