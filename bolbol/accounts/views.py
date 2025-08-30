from .models.user import User
from django.core.cache import cache
from .utils.generate_otp import generate_otp_code
from rest_framework.views import APIView, Response, status
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken


class OTPSenderAPIView(APIView):
    def post(self, request):
        phone_number = request.data.get("phone_number")
        otp_code = generate_otp_code()
        cache.set(phone_number, otp_code, timeout=300)

        print(f"Your OTP code is {otp_code}")

        return Response(
            {"message": "OTP sent successfully"},
            status=status.HTTP_200_OK
        )


class OTPVerifierAPIView(APIView):
    def post(self, request):
        phone_number = request.data.get("phone_number")
        otp_code = request.data.get("otp_code")
        cached_otp = cache.get(phone_number)

        if not cached_otp == otp_code:
            return Response(
                {"message": "Invalid OTP"},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        user = User.objects.get(phone_number=phone_number)
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        cache.delete(phone_number)

        return Response(
            {
                "detail": "Logged in successfully",
                "user_id": user.pk,
                "access": access_token,
                "refresh": str(refresh),
            }, status=status.HTTP_200_OK
        )
