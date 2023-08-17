from django.contrib import admin

from tour_guide_bulgaria.accounts.models import AppUser


@admin.register(AppUser)
class UserAdmin(admin.ModelAdmin):
    filter_horizontal = ('groups', 'user_permissions')
    list_display = ('username', 'is_staff', 'date_joined')

    def get_queryset(self, request):
        queryset = super(UserAdmin, self).get_queryset(request)
        queryset = queryset.order_by('date_joined')
        return queryset

