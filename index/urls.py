from django.urls import path
from .views import *


# Create your views here.

urlpatterns = [
    path('register/', registeration, name="register"),
    path('login',login,name="login"),
    path('activate/<uidb64>/<token>/', VerificationView.as_view(), name="activate"),
    path('details/<id>/', view_profile, name="profile_details"),
    path('profile_update/<id>/', update_profile, name="update-profile"),
    path('profile_delete/<id>/', delete_profile, name="delete-profile")
]