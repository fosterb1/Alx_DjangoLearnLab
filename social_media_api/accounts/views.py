from django.shortcuts import render, get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.models import Token
from rest_framework import status, generics, permissions
from django.contrib.auth import login, logout, get_user_model
from .serializers import UserRegistrationSerializer, UserLoginSerializer, UserProfileSerializer
from .models import User

# Alias for compatibility
CustomUser = get_user_model()

class UserRegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'message': 'User registered successfully.',
                'token': token.key,
                'user': UserProfileSerializer(user).data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            login(request, user)
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'message': 'User logged in successfully.',
                'token': token.key,
                'user': UserProfileSerializer(user).data
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserLogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()
        logout(request)
        return Response({'message': 'User logged out successfully.'}, status=status.HTTP_200_OK)
    
class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request):
        serializer = UserProfileSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'Profile updated successfully.',
                'data': serializer.data
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class FollowUserView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = CustomUser.objects.all()

    def post(self, request, user_id):
        user_to_follow = get_object_or_404(User, id=user_id)
        
        if user_to_follow == request.user:
            return Response(
                {'error': 'You cannot follow yourself.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if request.user.following.filter(id=user_id).exists():
            return Response(
                {'message': 'You are already following this user.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        request.user.following.add(user_to_follow)
        
        from notifications.models import Notification
        from django.contrib.contenttypes.models import ContentType
        Notification.objects.create(
            recipient=user_to_follow,
            actor=request.user,
            verb='started following you',
            target_content_type=ContentType.objects.get_for_model(user_to_follow),
            target_object_id=user_to_follow.id
        )
        
        return Response(
            {'message': f'You are now following {user_to_follow.username}.'},
            status=status.HTTP_200_OK
        )

class UnfollowUserView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = CustomUser.objects.all()

    def post(self, request, user_id):
        user_to_unfollow = get_object_or_404(User, id=user_id)
        
        if user_to_unfollow == request.user:
            return Response(
                {'error': 'You cannot unfollow yourself.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if not request.user.following.filter(id=user_id).exists():
            return Response(
                {'message': 'You are not following this user.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        request.user.following.remove(user_to_unfollow)
        return Response(
            {'message': f'You have unfollowed {user_to_unfollow.username}.'},
            status=status.HTTP_200_OK
        )
    