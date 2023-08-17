from django.views import generic as views
from django.contrib.auth import views as auth_views, authenticate, login
from django.contrib.auth import mixins as auth_mixins
from django.urls import reverse_lazy, reverse
from tour_guide_bulgaria.accounts.forms import CreateProfileForm, EditProfileForm, ChangePasswordForm, UserLoginForm
from tour_guide_bulgaria.accounts.models import Profile
from tour_guide_bulgaria.common.view_mixins import RedirectToDashboard
from tour_guide_bulgaria.web.models import Sight


class UserRegisterView(RedirectToDashboard, views.CreateView):
    form_class = CreateProfileForm
    template_name = 'accounts/home_no_profile.html'
    success_url = reverse_lazy('show dashboard')

    def form_valid(self, *args, **kwargs):
        result = super().form_valid(*args, **kwargs)
        login(self.request, self.object)
        return result


class UserLoginView(auth_views.LoginView):
    template_name = 'accounts/login_page.html'
    form_class = UserLoginForm
    success_url = reverse_lazy('show dashboard')

    def get_success_url(self):
        if self.success_url:
            return self.success_url
        return super().get_success_url()


class ChangeUserPasswordView(auth_views.PasswordChangeView):
    template_name = 'accounts/edit_password.html'
    form_class = ChangePasswordForm


class ProfileDetailsView(views.DetailView):
    model = Profile
    template_name = 'accounts/profile_details.html'
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_sights = list(Sight.objects.filter(user_id=self.object.user_id))

        user_sights_count = len(user_sights)

        context.update({
            'user_sights_count': user_sights_count,
            'is_owner': self.object.user_id == self.request.user.id,
            'user_sights': user_sights,
        })

        return context


class EditProfileView(views.UpdateView):
    model = Profile
    form_class = EditProfileForm

    template_name = 'accounts/edit_profile.html'

    def get_object(self):
        return self.request.user.profile

    def get_success_url(self):
        return reverse_lazy('profile details', kwargs={'pk': self.object.user_id})


class DeleteProfileView(views.DeleteView):
    model = Profile
    # form_class = DeleteProfileForm
    template_name = 'accounts/delete_profile.html'
    success_url = reverse_lazy('show index')
    # pk_url_kwarg = 'pk'

    def get_object(self):
        return self.request.user


class UserLogoutView(auth_views.LogoutView):
    next_page = reverse_lazy('show index')

