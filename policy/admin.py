from django.contrib import admin
from .models import Policy
from django_summernote.admin import SummernoteModelAdmin

   
class PolicyAdmin(SummernoteModelAdmin):
    summernote_fields = ('description',)
    list_display=(
        "title", "slug", "visible", 'sort',
        
        )

admin.site.register(Policy,PolicyAdmin)