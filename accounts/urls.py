from django.urls import path
from .views import RegisterView, LoginView, DeleteAccountView, ProfileUpdateView, LogoutView, manage_access_rule

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('delete-account/', DeleteAccountView.as_view(), name = 'delete-account'),
    path('profile/', ProfileUpdateView.as_view(), name = 'profile-update'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('access-rules/', manage_access_rule, name='manage-access-rules'),


]