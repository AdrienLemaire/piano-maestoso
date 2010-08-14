from django.contrib import admin
from models import Track

class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'artist', 'composer', 'category',  'description',
                    'added', 'adder')

admin.site.register(Track, TrackAdmin)
