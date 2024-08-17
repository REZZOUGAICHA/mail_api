
from django.urls import path
from .views import SendEmailView
#gmailapp
urlpatterns = [
    path('send/', SendEmailView.as_view(), name='send'),
]
