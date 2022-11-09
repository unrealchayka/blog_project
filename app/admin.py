from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin

from .models import *


class SomeModelAdmin(SummernoteModelAdmin):
    summernote_fields = '__all__'
     
    prepopulated_fields = {'slug' : ('title',)}


class CSomeModelAdmin(SummernoteModelAdmin):
    summernote_fields = 'text'
     
    prepopulated_fields = {'slug' : ('title_ru',)}



admin.site.register(Category)
admin.site.register(Post, SomeModelAdmin)
admin.site.register(Commet)
admin.site.register(City, CSomeModelAdmin)
admin.site.register(Star)
admin.site.register(Rating)
admin.site.register(CustomUser)