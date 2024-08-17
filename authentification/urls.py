from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.urls import path

urlpatterns = [
    path('gmailapp/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('gmailapp/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
