from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.contrib.auth import get_user_model, authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .serializers import UserSerializer
import re

User = get_user_model()

# Utility function to generate JWT tokens
def generate_tokens(user):
    refresh = RefreshToken.for_user(user)
    return {
        "access_token": str(refresh.access_token),
        "refresh_token": str(refresh)
    }

class UserAPIView(viewsets.ViewSet):
    """ViewSet for User CRUD operations"""

    permission_classes = [AllowAny]

    # CREATE USER
    @swagger_auto_schema(
        operation_description="Create a new user.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'first_name': openapi.Schema(type=openapi.TYPE_STRING, description='First name of the user'),
                'last_name': openapi.Schema(type=openapi.TYPE_STRING, description='Last name of the user'),
                'email': openapi.Schema(type=openapi.TYPE_STRING, description='Email of the user'),
                'username': openapi.Schema(type=openapi.TYPE_STRING, description='Username of the user'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description='Password of the user'),
            },
            required=['first_name', 'last_name', 'email', 'username', 'password']
        )
    )
    def create(self, request):
        """Create a new user"""
        # Extract password to validate
        password = request.data.get('password', '')

        # Password validations
        if len(password) < 8:
            return Response(
                {"message": "Password must be at least 8 characters long."},
                status=status.HTTP_400_BAD_REQUEST
            )
        if not re.search(r'[A-Z]', password):
            return Response(
                {"message": "Password must contain at least one uppercase character."},
                status=status.HTTP_400_BAD_REQUEST
            )
        if not re.search(r'\d', password):
            return Response(
                {"message": "Password must contain at least one number."},
                status=status.HTTP_400_BAD_REQUEST
            )
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            return Response(
                {"message": "Password must contain at least one special character."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Proceed with user creation
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.set_password(password)  # Hash the password
            user.save()
            return Response({"message": "User created successfully."}, status=status.HTTP_201_CREATED)
        return Response(serializer.messages, status=status.HTTP_400_BAD_REQUEST)

    # UPDATE USER
    @swagger_auto_schema(
        operation_description="Update user profile.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'first_name': openapi.Schema(type=openapi.TYPE_STRING, description='First name'),
                'last_name': openapi.Schema(type=openapi.TYPE_STRING, description='Last name'),
                'email': openapi.Schema(type=openapi.TYPE_STRING, description='Email address'),
            }
        )
    )
    def update(self, request, pk=None):
        """Update an existing user"""
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response({"message": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User updated successfully."}, status=status.HTTP_200_OK)
        return Response(serializer.messages, status=status.HTTP_400_BAD_REQUEST)

    # RETRIEVE SINGLE USER
    def retrieve(self, request, pk=None):
        """Retrieve a single user by ID"""
        try:
            user = User.objects.get(pk=pk)
            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"message": "User not found."}, status=status.HTTP_404_NOT_FOUND)

    # DELETE USER
    def destroy(self, request, pk=None):
        """Delete a user by ID"""
        try:
            user = User.objects.get(pk=pk)
            user.delete()
            return Response({"message": "User deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        except User.DoesNotExist:
            return Response({"message": "User not found."}, status=status.HTTP_404_NOT_FOUND)

    # LIST USERS
    def list(self, request):
        """List all users"""
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)



class LoginAPIView(viewsets.ViewSet):
    """ViewSet for User Login"""
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_description="Login endpoint for User",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING, description='Username of the user'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description='Password for authentication'),
            },
            required=['username', 'password']
        )
    )
    def create(self, request):
        """Authenticate and login a user"""
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response(
                {"message": "Both username and password are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = authenticate(request, username=username, password=password)
        if user:
            tokens = generate_tokens(user)
            return Response(
                {
                    "message": "Login successful.",
                    
                    "user_id": user.id,
                    "username": user.username,
                    "email": user.email,
                    
                    "access_token": tokens["access_token"],
                    "refresh_token": tokens["refresh_token"]
                },
                status=status.HTTP_200_OK
            )
        return Response(
            {"message": "Invalid credentials."},
            status=status.HTTP_401_UNAUTHORIZED
        )

class PasswordResetViewSet(viewsets.ViewSet):
    """
    ViewSet for Resetting User Password with Username Verification
    """

    @swagger_auto_schema(
        operation_description="Verify user legitimacy using the username.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['username'],
            properties={
                'username': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Username of the account."
                ),
            },
        )
    )
    def create(self, request):
        """
        Verify the legitimacy of the user using their username (POST method).
        """
        username = request.data.get('username')

        if not username:
            return Response(
                {"message": "Username is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user = User.objects.get(username=username)
            return Response(
                {"message": "User verified successfully.", "user_id": user.id},
                status=status.HTTP_200_OK
            )
        except User.DoesNotExist:
            return Response(
                {"message": "User not found."},
                status=status.HTTP_404_NOT_FOUND
            )

    @swagger_auto_schema(
        operation_description="Reset the password for the verified user by providing new password and confirm new password.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['user_id', 'new_password', 'confirm_new_password'],
            properties={
                'user_id': openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                    description="ID of the verified user."
                ),
                'new_password': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="New password for the account."
                ),
                'confirm_new_password': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Confirmation of the new password."
                ),
            },
        )
    )
    def update(self, request, pk=None):
        """
        Reset password for a verified user (PUT method).
        """
        user_id = request.data.get('user_id')
        new_password = request.data.get('new_password')
        confirm_new_password = request.data.get('confirm_new_password')

        if not user_id or not new_password or not confirm_new_password:
            return Response(
                {"message": "User ID, new password, and confirm new password are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if new_password != confirm_new_password:
            return Response(
                {"message": "New passwords do not match."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if len(new_password) < 8:
            return Response(
                {"message": "New password must be at least 8 characters long."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not re.search(r'[A-Z]', new_password):
            return Response(
                {"message": "New password must contain at least one uppercase character."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not re.search(r'\d', new_password):
            return Response(
                {"message": "New password must contain at least one number."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', new_password):
            return Response(
                {"message": "New password must contain at least one special character."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user = User.objects.get(pk=user_id)
            user.set_password(new_password)  # Using Django's set_password for proper hashing
            user.save()
            return Response(
                {"message": "Password reset successfully."},
                status=status.HTTP_200_OK
            )
        except User.DoesNotExist:
            return Response(
                {"message": "User not found."},
                status=status.HTTP_404_NOT_FOUND
            )
