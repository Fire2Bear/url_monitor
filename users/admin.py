from django.contrib import admin

from users.models import UserProfile


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', )
    list_filter = ['username', ]
    list_editable = []
    search_fields = ['username', 'email', 'display_name', ]


admin.site.register(UserProfile, UserProfileAdmin)
