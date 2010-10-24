# -*- coding:Utf-8 -*-

# from python
#from optparse import make_option
#from subprocess import call
import commands

# from django
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
#from django.core.management.base import CommandError

# from project
from django.conf import settings

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
        logger.info(commands.getoutput('%s --videoquality 5 '
           '--audioquality 1 --videobitrate 200 --output '
           '/tmp/%s.ogv %s' % (settings.FFMPEG2THEORA_PATH, filename, input)))
    else:
        logger.info(commands.getoutput('%s -i %s -sameq /tmp/%s.%s' % (settings.FFMPEG_PATH, input, filename, fileext)))
    #Open the file and put it in a friendly format to save the image
    f = open('/tmp/%s.%s' % (filename, fileext), 'r')
    filecontent = ContentFile(f.read())
    f.close()
    logger.info(track.__getattribute__("track_%s" % fileext).save('%s.%s' % (filename, fileext), filecontent , save=True))
    if not track.image and fileext == "mp4":
        logger.info(commands.getoutput('%s -i /tmp/%s.%s -vframes 1 -ss 10 /tmp/%s1.png' % (settings.FFMPEG_PATH, filename, fileext, filename)))
        f = open('/tmp/%s1.png' % filename, 'r')
        filecontent = ContentFile(f.read())
        f.close()
        image = Photo(title=filename, title_slug=filename)
        logger.info("image : %s (filename: %s)" % (image, filename))
        image.image.save('%s.png' % filename, filecontent , save=True)
        logger.info("image saved")
        image.save()
        track.image = image
    logger.info(commands.getoutput("rm /tmp/%s1.png" % filename))
    #Clean the flv and png files left around
    #call("find . -maxdepth 1 -type f -name '*." + fileext + "' -o -name '*.png' | xargs rm", shell=True)
    logger.info(commands.getoutput("rm /tmp/*.%s" % fileext))
    track.save()
    logger.info('Converted' + track.__getattribute__("track_" + fileext).file.name)


def convert(options, args):
    """
    Converts the track to flv format using settings.FFMPEG_PATH and creates a stil for preview
    """
    #reset = options.get('reset', None)

    #print 'Converting tracks, this may take a while...'
    #print "avant modif :" + os.environ['PATH']
    #os.environ['PATH'] += ":/usr/local/lib/"
    #print "apres modif :" + os.environ['PATH']

    for track in Track.objects.all():
        #Convert the vidoes using settings.FFMPEG_PATH
        if not args:
            raise Exception("You should add an argument : [mp4|webm|ogv]")
        #if not track.__getattribute__("track_" + args[0]):
        _convert(track, args[0])
        #else:
           #pass
