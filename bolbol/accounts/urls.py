from django.urls import path
from .views import OTPSenderAPIView, OTPVerifierAPIView


urlpatterns = [
    path(
        "send-otp/",
        OTPSenderAPIView.as_view(),
        name="send-otp"
    ),
    path(
        "verify-otp/",
        OTPVerifierAPIView.as_view(),
        name="verify-otp"
    )
]