from django.contrib import admin
from models import Track

class TrackAdmin(admin.ModelAdmin):
    list_display = ('title', 'artist', 'composer', 'category',  'description',
                    'added', 'adder')

admin.site.register(Track, TrackAdmin)
