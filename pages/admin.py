from django.contrib import admin

from pages.models import Page


class PageAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'url', )
    list_filter = ['user__username', ]
    list_editable = ['title', 'url', ]
    search_fields = ['user__username', 'title', 'url', ]


admin.site.register(Page, PageAdmin)
