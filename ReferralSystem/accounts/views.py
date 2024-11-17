from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import User
from .serializers import UserSerializer, LoginSerializer, ReferralSerializer
from django.contrib.auth import authenticate
from django.contrib.auth import authenticate
from rest_framework import serializers


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']

            # Use custom authentication to authenticate with email
            user = authenticate(request=request,email=email, password=password)
            if user:
                # Successfully authenticated
                return Response({'message': 'Login successful', 'user_id': user.id}, status=status.HTTP_200_OK)
            else:
                # Authentication failed
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ReferralView(APIView):
    
    def get(self, request):
        # Check if the referral_code query parameter is passed
        referral_code = request.query_params.get('referral_code', None)
        
        if not referral_code:
            return Response({'error': 'referral_code parameter is required'}, status=status.HTTP_400_BAD_REQUEST)

        # Get users who registered using the provided referral_code
        users = User.objects.filter(referral_code=referral_code)
        
        if not users.exists():
            return Response({'error': 'No users found who registered with this referral code'}, status=status.HTTP_404_NOT_FOUND)

        # Serialize the users and return them in the response
        serializer = ReferralSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
