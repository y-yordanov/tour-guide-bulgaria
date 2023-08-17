import os

from django import forms

from tour_guide_bulgaria.web.helpers import DisabledFieldsFormMixin
from tour_guide_bulgaria.web.models import Sight, Category, SightComment, SightLike

NATURE = "Nature"
FORTRESS = "Fortress"
SPIRITUAL = "Spiritual"
TRADITIONAL = 'Traditional'
OTHER = "Other"
CATEGORIES = [(x, x) for x in (NATURE, FORTRESS, SPIRITUAL, TRADITIONAL, OTHER)]

WIDGETS_OBJECT = {
            'name_of_sight': forms.TextInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'cols': 30, 'rows': 4}),
            'category': forms.Select(choices=CATEGORIES, attrs={'class': 'form-control'}),
            'pros': forms.Textarea(attrs={'class': 'form-control', 'cols': 30, 'rows': 2}),
            'cons': forms.Textarea(attrs={'class': 'form-control', 'cols': 30, 'rows': 2}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }


class AddSightForm(forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

    def save(self, commit=True):
        sight = super().save(commit=False)

        sight.user = self.user
        if commit:
            sight.save()

        return sight

    class Meta:
        model = Sight
        fields = ('name_of_sight', 'location', 'description', 'category', 'pros', 'cons', 'image')
        widgets = WIDGETS_OBJECT


class EditSightForm(forms.ModelForm):
    class Meta:
        model = Sight
        exclude = ('user', )
        widgets = WIDGETS_OBJECT


class DeleteSightForm(DisabledFieldsFormMixin, forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        if commit:
            SightLike.objects.filter(sight_id=self.instance.id) \
                .delete()
            SightComment.objects.filter(sight_id=self.instance.id) \
                .delete()
            image_path = self.instance.image.path
            os.remove(image_path)
            self.instance.delete()

        return self.instance


# class SightCommentForm(forms.ModelForm):
#     class Meta:
#         model = SightComment
#         fields = ('body',)
#         widgets = {'body': forms.Textarea(attrs={'class': 'form-control', 'cols': 30, 'rows': 4})}
#         labels = {
#             "body": ""
#         }

class SightCommentForm(forms.ModelForm):
    body = forms.CharField(
        label='',
        widget=forms.Textarea(attrs={'class': 'form-control', 'cols': 30, 'rows': 4})
    )

    class Meta:
        model = SightComment
        fields = ('body',)


class DeleteProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        self.instance.delete()
        return self.instance
