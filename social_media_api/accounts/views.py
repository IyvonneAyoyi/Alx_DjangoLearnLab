from rest_framework import generics, permissions  # ADD 'permissions' HERE
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from .models import CustomUser
from .serializers import UserSerializer, LoginSerializer
from django.contrib.auth import authenticate

class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]  # ADD THIS

class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [permissions.AllowAny]  # ADD THIS

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(username=serializer.validated_data['username'], password=serializer.validated_data['password'])
        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key})
        return Response({'error': 'Invalid Credentials'}, status=400)

# Profile View to retrieve and update user profile
class UserProfileView(generics.RetrieveUpdateAPIView):  # FIX INDENTATION
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]  # This should work now

    def get_object(self):
        return self.request.user  # Return the currently logged-in user