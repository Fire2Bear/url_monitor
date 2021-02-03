from django.contrib import admin

from verification_results.models import VerificationResult


class VerificationResultAdmin(admin.ModelAdmin):
    list_display = ('date', 'verification', 'success', 'description', )
    list_filter = ['date', 'success', 'verification', ]
    list_editable = []
    search_fields = ['date',
                     'success',
                     'verification',
                     'verification__page__title',
                     'verification__page__url',
                     'verification__verification_type__name',
                     'verification__verification_option',
                     ]
    ordering = ("-date", "verification__page", "success")


admin.site.register(VerificationResult, VerificationResultAdmin)
