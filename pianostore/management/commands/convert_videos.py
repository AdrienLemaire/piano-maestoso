# from python
from optparse import make_option
from subprocess import call

# from django
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand, CommandError

# from apps
from pianostore.models import Track
from photologue.models import Photo


class Command(BaseCommand):
    #option_list = BaseCommand.option_list + (
        #make_option('--reset', '-r', action='store_true', dest='reset', help='Convert tracks even if they existed'),
    #)

    help = ('Converts track to the required web format.')
    args = ''

    requires_model_validation = True
    can_import_settings = True

    def handle(self, *args, **options):
        return convert(options)


def _convert(track, fileext)
    print call('ffmpeg -i %s -sameq %s.%s' % (input, filename, fileext), shell=True)
    #Open the file and put it in a friendly format for image save
    f = open('%s.%s' % (filename, fileext), 'r')
    filecontent = ContentFile(f.read())
    track.track.save('%s.%s' % (filename, fileext), filecontent , save=True)
    f.close()
    if track.image:
        pass
    else:
        print call('ffmpeg -i %s.%s -sameq %s%sd.png' % (filename, fileext, filename, '%'), shell=True)
        f = open('%s1.png' % filename, 'r')
        filecontent = ContentFile(f.read())
        image = Photo(title=filename, title_slug=filename)
        image.image.save('%s1.png' % filename, filecontent , save=True)
        image.save()
        track.image = image
    #Clean the flv and png files left around
    call("find . -maxdepth 1 -type f -name '*.flv' -o -name '*.png' | xargs rm", shell=True)
    track.save()
    print 'Converted' + track.track.file.name


def convert(options):
    """
    Converts the track to flv format using ffmpeg and creates a stil for preview
    """
    #reset = options.get('reset', None)

    print 'Converting tracks, this may take a while...'

    for track in Track.objects.all():
        filename =  track.title_slug
        input = track.original_track.file.name
        print 'Original: ' + input
        #Convert the vidoes using ffmpeg
        if not track.track_mp4:
            _convert(track, "mp4")
        elif not track.track_webm:
            _convert(track, "webm")
        elif not track.track_ogv:
            _convert(track, "ogv")
        else:
           pass
