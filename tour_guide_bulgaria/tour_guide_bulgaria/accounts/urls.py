from django.urls import path, reverse_lazy
from django.views.generic import RedirectView

from tour_guide_bulgaria.accounts.views import UserLoginView, UserRegisterView, UserLogoutView, ProfileDetailsView, \
    EditProfileView, DeleteProfileView, ChangeUserPasswordView

urlpatterns = (
    path('login/', UserLoginView.as_view(), name='login user'),
    path('register/', UserRegisterView.as_view(), name='register'),
    path('logout/', UserLogoutView.as_view(), name='logout user'),

    path('<int:pk>/', ProfileDetailsView.as_view(), name='profile details'),
    path('edit-password/', ChangeUserPasswordView.as_view(), name='edit password'),
    path('password_change_done/', RedirectView.as_view(url=reverse_lazy('show dashboard')), name='password_change_done'),
    path('profile/edit/<int:pk>/', EditProfileView.as_view(), name='edit profile'),
    path('profile/delete/<int:pk>/', DeleteProfileView.as_view(), name='delete profile'),
    )


