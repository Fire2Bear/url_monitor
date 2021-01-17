from django.contrib import admin

from verifications.models import Verification


class VerificationAdmin(admin.ModelAdmin):
    list_display = ('page', 'verification_type', 'verification_option', )
    list_filter = ['verification_type__name', 'page__title', ]
    list_editable = []
    search_fields = ['page__title', 'page__url', 'verification_type__name', 'verification_option', ]


admin.site.register(Verification, VerificationAdmin)
