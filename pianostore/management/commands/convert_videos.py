# from python
from optparse import make_option
from subprocess import call
import commands

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
        return convert(options, args)


def _convert(track, fileext, logger):
    filename =  track.title_slug
    input = track.original_track.file.name
    if fileext == "ogv":
        logger.info(commands.getoutput('ffmpeg2theora --videoquality 5 '
           '--audioquality 1 --videobitrate 200 --max_size 320x240 --output '
           '/tmp/%s.ogv %s' % (filename, input)))
    else:
        logger.info('/usr/local/bin/ffmpeg -i %s -sameq /tmp/%s.%s' % (input, filename, fileext))
        call('/usr/local/bin/ffmpeg -i %s -sameq /tmp/%s.%s' % (input, filename, fileext), shell=True)
    logger.info("open('/tmp/%s.%s' % (" + filename + ", " + fileext + "), 'r')")
    #Open the file and put it in a friendly format to save the image
    f = open('/tmp/%s.%s' % (filename, fileext), 'r')
    filecontent = ContentFile(f.read())
    logger.info("%s adds track_%s fields" % (track, fileext))
    track.__getattribute__("track_" + fileext).save('%s.%s' % (filename, fileext), filecontent , save=True)
    logger.info("video done")
    f.close()
    if track.image:
        pass
    else:
        #logger.info('/usr/local/bin/ffmpeg -i /tmp/%s.%s -vframes 1 -ss 10 /tmp/%s1.png' % (filename, fileext, filename))
        #call('/usr/local/bin/ffmpeg -i /tmp/%s.%s -vframes 1 -ss 10 /tmp/%s1.png' % (filename, fileext, filename), shell=True)
        logger.info("About to execute commands.getoutput ...")
        logger.info(commands.getoutput('/usr/local/bin/ffmpeg -i /tmp/%s.%s -vframes 1 -ss 10 /tmp/%s1.png' % (filename, fileext, filename)))
        logger.info("commands.getoutput done. About to open the file...")
        f = open('/tmp/%s1.png' % filename, 'r')
        filecontent = ContentFile(f.read())
        image = Photo(title=filename, title_slug=filename)
        image.image.save('%s.png' % filename, filecontent , save=True)
        image.save()
        track.image = image
    #Clean the flv and png files left around
    #call("find . -maxdepth 1 -type f -name '*." + fileext + "' -o -name '*.png' | xargs rm", shell=True)
    call("rm /tmp/*." + fileext + " *.png *.stt", shell=True)
    track.save()
    logger.info('Converted' + track.__getattribute__("track_" + fileext).file.name)


def convert(options, args):
    """
    Converts the track to flv format using /usr/local/bin/ffmpeg and creates a stil for preview
    """
    #reset = options.get('reset', None)

    #print 'Converting tracks, this may take a while...'
    #print "avant modif :" + os.environ['PATH']
    #os.environ['PATH'] += ":/usr/local/lib/"
    #print "apres modif :" + os.environ['PATH']

    for track in Track.objects.all():
        #Convert the vidoes using /usr/local/bin/ffmpeg
        if not args:
            raise Exception("You should add an argument : [mp4|webm|ogv]")
        #if not track.__getattribute__("track_" + args[0]):
        _convert(track, args[0])
        #else:
           #pass
