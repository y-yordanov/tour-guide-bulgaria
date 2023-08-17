from django.contrib import admin

from tour_guide_bulgaria.web.models import Sight, Category, SightComment


@admin.register(Sight)
class SightAdmin(admin.ModelAdmin):
    list_display = ('name_of_sight', 'location')
    search_fields = ('name_of_sight', 'location')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(SightComment)
class SightCommentAdmin(admin.ModelAdmin):
    list_display = ('sight', 'user')
