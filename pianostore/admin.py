from django.contrib import admin
from models import Track


class TrackAdmin(admin.ModelAdmin):
    list_display = ('original_track', 'title', 'title_slug', 'artist',
                    'composer', 'category', 'description', 'date_added',
                    'adder', 'image')


admin.site.register(Track, TrackAdmin)
