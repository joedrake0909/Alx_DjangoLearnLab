from django.shortcuts import render
from rest_framework import status, generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, get_user_model
from .serializers import UserRegistrationSerializer, UserLoginSerializer, UserProfileSerializer

User = get_user_model()

# Create your views here.

class UserRegistrationView(generics.CreateAPIView):
    """
    API view for user registration.
    Returns authentication token upon successful registration.
    """
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = Token.objects.get(user=user)
        
        return Response({
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
            },
            'token': token.key,
            'message': 'User registered successfully'
        }, status=status.HTTP_201_CREATED)


class UserLoginView(APIView):
    """
    API view for user login.
    Returns authentication token upon successful login.
    """
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        
        user = authenticate(username=username, password=password)
        
        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                },
                'token': token.key,
                'message': 'Login successful'
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'error': 'Invalid credentials'
            }, status=status.HTTP_401_UNAUTHORIZED)


class UserProfileView(generics.RetrieveUpdateAPIView):
    """
    API view for retrieving and updating user profile.
    Requires authentication.
    """
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        return self.request.user
