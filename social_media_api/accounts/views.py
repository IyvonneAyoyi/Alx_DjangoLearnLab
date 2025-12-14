from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from .models import CustomUser
from .serializers import UserSerializer, LoginSerializer
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404

class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(username=serializer.validated_data['username'], password=serializer.validated_data['password'])
        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key})
        return Response({'error': 'Invalid Credentials'}, status=400)

class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

# ADD  NEW VIEWS FOR FOLLOW FUNCTIONALITY

class FollowUserView(APIView):
    """
    View to follow another user
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, user_id):
        user_to_follow = get_object_or_404(CustomUser, id=user_id)
        
        # Check if trying to follow self
        if user_to_follow == request.user:
            return Response(
                {'error': 'You cannot follow yourself'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Check if already following
        if request.user.following.filter(id=user_id).exists():
            return Response(
                {'error': f'You are already following {user_to_follow.username}'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Follow the user
        request.user.following.add(user_to_follow)
        return Response({
            'message': f'You are now following {user_to_follow.username}',
            'following_count': request.user.following.count()
        }, status=status.HTTP_200_OK)

class UnfollowUserView(APIView):
    """
    View to unfollow a user
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, user_id):
        user_to_unfollow = get_object_or_404(CustomUser, id=user_id)
        
        # Check if actually following
        if not request.user.following.filter(id=user_id).exists():
            return Response(
                {'error': f'You are not following {user_to_unfollow.username}'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Unfollow the user
        request.user.following.remove(user_to_unfollow)
        return Response({
            'message': f'You have unfollowed {user_to_unfollow.username}',
            'following_count': request.user.following.count()
        }, status=status.HTTP_200_OK)