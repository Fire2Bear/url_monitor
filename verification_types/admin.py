from django.contrib import admin

from verification_types.models import VerificationType


class VerificationTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'identifiant', 'description', )
    list_filter = ['name', 'identifiant', ]
    list_editable = ['name', 'description', ]
    search_fields = ['name', 'identifiant', 'description', ]


admin.site.register(VerificationType, VerificationTypeAdmin)
