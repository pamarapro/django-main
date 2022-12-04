from django.contrib import admin
from .models import Data
from django_summernote.admin import SummernoteModelAdmin

class DataAdmin(SummernoteModelAdmin):
    summernote_fields = ('services','header_text','footer_content')
   
admin.site.register(Data, DataAdmin)