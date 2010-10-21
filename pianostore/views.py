# from python
#from time import sleep
import os
import logging

# from django
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.http import HttpResponseRedirect
from django.http import HttpResponse, HttpResponseBadRequest
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

# from project
from django.conf import settings

# from app
from models import Track
from forms import TrackForm
from tasks import html5_videos_convert
from tasks import rotate_video


def tracks(request):
    """ Return the all tracks list, ordered by added date. """
    tracks = Track.objects.all().order_by("-date_added")
    return render_to_response("pianostore/tracks.html", {
        "tracks": tracks,
        "list": 'all',
    }, context_instance=RequestContext(request))


def user_tracks(request, username):
    """ Return an user tracks list. """
    user = get_object_or_404(User, username=username)
    usertracks = Track.objects.filter(adder=user).order_by("-date_added")
    return render_to_response("pianostore/tracks.html", {
        "tracks": usertracks,
        "list": 'user',
        "username": username,
    }, context_instance=RequestContext(request))


def track(request, track_id):
    """ Return a track given its id. """
    isyours = False
    track = Track.objects.get(id=track_id)
    if request.user == track.adder:
        isyours = True
    return render_to_response("pianostore/track.html", {
        "track": track,
        "isyours": isyours,
    }, context_instance=RequestContext(request))


@login_required
def your_tracks(request):
    """ Return the logged user tracks list. """
    yourtracks = Track.objects.filter(adder=request.user)\
        .order_by("-date_added")
    return render_to_response("pianostore/tracks.html", {
        "tracks": yourtracks,
        "list": 'yours',
    }, context_instance=RequestContext(request))


@login_required
def add_track(request):
    """ Add a track to the pianostore. """
    track_form = TrackForm()

    if request.method == "POST":
        # With runserver or uwsgi
        #track_form = TrackForm(request.user, request.POST, request.FILES)
        # With nginx upload
        track_form = TrackForm(request.user, request.POST)
        logging.info("POST:%s\nFILES:%s" % (request.POST, request.FILES))
        if track_form.is_valid():
            new_track = track_form.save(commit=False)
            new_track.adder = request.user
            new_track.original_track = os.path.join(settings.UPLOAD_URL,
                    request.POST['original_track.name'])
            new_track.save()

            # The video process should be done like this :
                #- ffmpeg convert to avi            <= These 2 parts can be avoid
                #- mencode rotate the video         <= if no rotation needed
                #- ffmpeg2theora convert to ogv
                #- ffmpeg convert to mp4 and webm
            rotate_video(
                request.POST['original_track.path'],
                request.POST['original_track.name'],
                request.POST['rotation']
            )
            for fileext in ["mp4", "ogv", "webm"]:
                html5_videos_convert.delay(fileext, new_track.original_track)

            request.user.message_set.create(message=_("You have successfully "
                "uploaded track '%(title)s'") % {'title': new_track.title})
            return HttpResponseRedirect(reverse("pianostore.views.tracks"))
    return render_to_response("pianostore/add.html", {
        "track_form": track_form,
    }, context_instance=RequestContext(request))


@login_required
def update_track(request, track_id):
    """ Update a track given its id. """
    track = Track.objects.get(id=track_id)
    if request.method == "POST":
        track_form = TrackForm(request.user, request.POST, request.FILES,
                               instance=track)
        track_form.is_update = True
        if request.user == track.adder:
            if track_form.is_valid():
                track_form.save()
                request.user.message_set.create(message=_("You have updated "
                              "track '%(title)s'") % {'title': track.title})
                return HttpResponseRedirect(reverse("pianostore.views.tracks"))
    else:
        track_form = TrackForm(instance=track)
        return render_to_response("pianostore/update.html", {
            "track_form": track_form,
            "track": track,
            }, context_instance=RequestContext(request))


@login_required
def delete_track(request, track_id):
    """ Delete a track given its id. """
    track = get_object_or_404(Track, id=track_id)
    if request.user == track.adder:
        track.delete()
        request.user.message_set.create(message=_("Track Deleted"))

    return HttpResponseRedirect(reverse("pianostore.views.tracks"))


def upload_progress(request):
    """
    Return JSON object with information about the progress of an upload.
    """
    progress_id = None
    if 'X-Progress-ID' in request.GET:
        progress_id = request.GET['X-Progress-ID']
    elif 'X-Progress-ID' in request.META:
        progress_id = request.META['X-Progress-ID']
    if progress_id:
        from django.utils import simplejson
        cache_key = "%s_%s" % (request.META['REMOTE_ADDR'], progress_id)
        data = cache.get(cache_key)
        json = simplejson.dumps(data)
        return HttpResponse(json)
    else:
        return HttpResponseBadRequest('Server Error: You must provide X-Progress-ID header or query param.')

