#from django
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

#from piano
from models import Track
from forms import TrackForm


def tracks(request):
    """ Return the all tracks list, ordered by added date. """
    tracks = Track.objects.all().order_by("-added")
    return render_to_response("piano/tracks.html", {
        "tracks": tracks,
        "list": 'all',
    }, context_instance=RequestContext(request))


def user_tracks(request, username):
    """ Return an user tracks list. """
    user = get_object_or_404(User, username=username)
    usertracks = Track.objects.filter(adder=user).order_by("-added")
    return render_to_response("piano/tracks.html", {
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
    return render_to_response("piano/track.html", {
        "track": track,
        "isyours": isyours,
    }, context_instance=RequestContext(request))


@login_required
def your_tracks(request):
    """ Return the logged user tracks list. """
    yourtracks = Track.objects.filter(adder=request.user).order_by("-added")
    return render_to_response("piano/tracks.html", {
        "tracks": yourtracks,
        "list": 'yours',
    }, context_instance=RequestContext(request))


@login_required
def add_track(request):
    """ Add a track to the piano. """
    # POST request
    if request.method == "POST":
        track_form = TrackForm(request.POST, request.FILES)
        if track_form.is_valid():
            # from ipdb import set_trace; set_trace()
            new_track = track_form.save(commit=False)
            new_track.adder = request.user
            new_track.save()
            request.user.message_set.create(message=_("You have saved track "
                                  "'%(title)s'") % {'title': new_track.title})
            return HttpResponseRedirect(reverse("piano.views.tracks"))
    # GET request
    else:
        track_form = TrackForm()
        return render_to_response("piano/add.html", {
            "track_form": track_form,
            }, context_instance=RequestContext(request))
    # generic case
    return render_to_response("piano/add.html", {
        "track_form": track_form,
    }, context_instance=RequestContext(request))


@login_required
def update_track(request, track_id):
    """ Update a track given its id. """
    track = Track.objects.get(id=track_id)
    if request.method == "POST":
        track_form = TrackForm(request.POST, request.FILES, instance=track)
        track_form.is_update = True
        if request.user == track.adder:
            #from ipdb import set_trace; set_trace()
            if track_form.is_valid():
                track_form.save()
                request.user.message_set.create(message=_("You have updated "
                              "track '%(title)s'") % {'title': track.title})
                return HttpResponseRedirect(reverse("piano.views.tracks"))
    else:
        track_form = TrackForm(instance=track)
        return render_to_response("piano/update.html", {
            "track_form": track_form,
            "track": track,
            }, context_instance=RequestContext(request))


@login_required
def delete_track(request, track_id):
    """ Delete a track given its id. """
    track = get_object_or_404(Track, id=track_id)
    if request.user == track.adder:
        track.delete()
        request.user.message_set.create(message="Track Deleted")

    return HttpResponseRedirect(reverse("piano.views.tracks"))
