#from django
from django.conf.urls.defaults import *

# from piano
from models import Track

urlpatterns = patterns('',
        url(r'^$', 'piano.views.tracks', name="all_tracks"),
        url(r'^(d+)/track/$', 'piano.views.track', name="describe_track"),
        url(r'^your_tracks/$', 'piano.views.your_tracks', name="your_tracks"),
        url(r'^user_tracks/(?P<username>w+)/$', 'piano.views.user_tracks', name="user_tracks"),
        # CRUD urls
        url(r'^add/$', 'piano.views.add_track', name="add_track"),
        url(r'^(d+)/update/$', 'piano.views.update_track', name="update_track"),
        url(r'^(d+)/delete/$', 'piano.views.delete_track', name="delete_track"),
    )
