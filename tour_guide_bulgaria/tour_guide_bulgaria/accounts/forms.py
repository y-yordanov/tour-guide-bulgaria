from django import forms
from django.contrib.auth import forms as auth_forms, get_user_model
from django.core.validators import MinLengthValidator, MinValueValidator
from tour_guide_bulgaria.accounts.models import Profile

from tour_guide_bulgaria.common.validators import validate_only_letters


class CreateProfileForm(auth_forms.UserCreationForm):
    first_name = forms.CharField(
        max_length=Profile.FIRST_NAME_MAX_LENGTH,
        validators=(
            MinLengthValidator(Profile.FIRST_NAME_MIN_LENGTH),
            validate_only_letters,
        )
    )

    last_name = forms.CharField(
        max_length=Profile.LAST_NAME_MAX_LENGTH,
        validators=(
            MinLengthValidator(Profile.LAST_NAME_MIN_LENGTH),
            validate_only_letters,
        )
    )
    age = forms.IntegerField(
        validators=(
            MinValueValidator(Profile.AGE_MIN_VALUE),
        )
    )
    about = forms.CharField(
        widget=forms.Textarea,
    )
    profile_image = forms.ImageField(
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'name': 'username',
            'type': 'text',
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'name': 'password',
            'type': 'password',
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'name': 'password',
            'type': 'password',
        })
        self.fields['first_name'].widget.attrs.update({
            'class': 'form-control',
            'name': 'first_name',
            'type': 'textinput',
        })
        self.fields['last_name'].widget.attrs.update({
            'class': 'form-control',
            'name': 'last_name',
            'type': 'text',
        })
        self.fields['age'].widget.attrs.update({
            'class': 'form-control',
            'name': 'age',
            'type': 'number',
        })
        self.fields['about'].widget.attrs.update({
            'class': 'form-control',
            'name': 'about',
            'type': 'textarea',
            'cols': 10,
            'rows': 2,
        })
        self.fields['profile_image'].widget.attrs.update({
            'class': 'form-control',
            'name': 'profile_image',
            'type': 'file',
        })

    def save(self, commit=True):
        user = super().save(commit=commit)

        profile = Profile(
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
            age=self.cleaned_data['age'],
            about=self.cleaned_data['about'],
            profile_image=self.cleaned_data['profile_image'],
            user=user,
        )
        if commit:
            profile.save()
        return user

    class Meta:
        model = get_user_model()
        fields = ('username', 'password1', 'password2', 'first_name', 'last_name', 'age', 'about', 'profile_image')


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('first_name', 'last_name', 'age', 'about', 'profile_image')
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'age': forms.NumberInput(attrs={'class': 'form-control'}),
            'about': forms.Textarea(attrs={'class': 'form-control', 'cols': 30, 'rows': 2}),
            'profile_image': forms.FileInput(attrs={'class': 'form-control'}),
        }


class UserLoginForm(auth_forms.AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'name': 'username',
            'type': 'text',
        })
        self.fields['password'].widget.attrs.update({
            'class': 'form-control',
            'name': 'password',
            'type': 'password',
        })

    class Meta:
        fields = ('username', 'password')


class ChangePasswordForm(auth_forms.PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['old_password'].widget.attrs.update({
            'class': 'form-control',
            'name': 'old_password',
            'type': 'password',
        })
        self.fields['new_password1'].widget.attrs.update({
            'class': 'form-control',
            'name': 'new_password1',
            'type': 'password',
        })
        self.fields['new_password2'].widget.attrs.update({
            'class': 'form-control',
            'name': 'new_password2',
            'type': 'password',
        })

    class Meta:
        fields = ('old_password', 'new_password1', 'new_password2')


