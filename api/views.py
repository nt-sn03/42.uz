from django.core.cache import cache

from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken

from .bot import handle_update, set_webhook
from .serializers import WebhookSerializer, LoginSerializer
from .models import User


class HandleUpdateView(APIView):
    def post(self, request: Request) -> Response:
        # Here you would handle the incoming update from Telegram
        # For example, you could parse the update and respond accordingly
        update_data = request.data
        # Process the update_data as needed
        print("Received update:", update_data)

        # Call the function to handle the update
        handle_update(update_data)
        
        # Respond with a success status
        return Response({"message": "Update received successfully"}, status=status.HTTP_200_OK)


class SetWebhookView(APIView):
    def post(self, request: Request) -> Response:
        serializer = WebhookSerializer(data=request.data)
        if serializer.is_valid():
            webhook_url = serializer.validated_data['webhook_url']
            set_webhook(webhook_url)
            # Respond with a success status
            return Response({"message": "Webhook set successfully"}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class LoginView(APIView):
    def post(self, request: Request) -> Response:
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            otp = serializer.validated_data['otp']
            # Here you would validate the OTP and log the user in
            user_id = cache.get(f'user_{otp}')

            user = User.objects.filter(username=user_id).first()
            if user:
                cache.delete(f"user_{otp}")  # Invalidate the OTP after use
                cache.delete(f"otp_{user_id}")  # Remove the OTP from cache
                # Generate JWT tokens
                access_token = AccessToken.for_user(user)
                refresh_token = RefreshToken.for_user(user)
                
                return Response({
                    "access": str(access_token),
                    "refresh": str(refresh_token)
                }, status=status.HTTP_200_OK)
            
            else:
                return Response({"message": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST)
            
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            