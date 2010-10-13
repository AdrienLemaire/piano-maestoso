#from django
from django.conf.urls.defaults import *

# from pianostore
#from models import Track

urlpatterns = patterns('pianostore.views',
        url(r'^$', 'tracks', name="all_tracks"),
        url(r'^(\d+)/track/$', 'track', name="describe_track"),
        url(r'^your_tracks/$', 'your_tracks', name="your_tracks"),
        url(r'^user_tracks/(?P<username>\w+)/$', 'user_tracks',
            name="user_tracks"),
        # CRUD urls
        url(r'^add/$', 'add_track', name="add_track"),
        url(r'^(\d+)/update/$', 'update_track',
            name="update_track"),
        url(r'^(\d+)/delete/$', 'delete_track',
            name="delete_track"),
    )
