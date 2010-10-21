# from python
import commands
import logging
import os
import shutil

# from project
from celery.decorators import task#periodic_task, task
#from celery.task.schedules import crontab
from django.conf import settings

# from app
from pianostore.management.commands.convert_videos import _convert
from pianostore.models import Track


def _convert_video(type_video):
    log_file = os.path.join(settings.LOG_DIR, "convert_%s.log" % type_video)
    logging.basicConfig(filename=log_file,level=logging.DEBUG)
    for track in Track.objects.all():
        if not track.__getattribute__("track_%s" % type_video):
            logging.debug("_convert(%s, %s) ..." % (track, type_video))
            _convert(track, type_video)
        else:
            logging.debug("%s not converted" % track)

def _move_video(path, filename):
    shutil.move(path, os.path.join(settings.UPLOAD_DIR, filename))

#@periodic_task(run_every=crontab(hour="*", minute="*", day_of_week="*"))
#def convert_mp4():
    #_convert_video("mp4")

@task
def rotate_video(filepath, filename, angle):
    logger = rotate_video.get_logger()
    angleToNb = {
        "90" : "1",
        "270" : "2",
    }
    if angle and angle in angleToNb.keys():
        logger.info("video %s rotated to %s degres" % (filename, angle))
        rotate_nb = angleToNb[angle]
        logger.info(commands.getoutput('%s -i %s -sameq /tmp/%s_temp.avi' %
            (settings.FFMPEG_PATH, filepath, filename)))
        logger.info(commands.getoutput('''%s -vf rotate=%s -o /tmp/%s.avi -oac
                        copy -ovc lavc -lavcopts vcodec=mjpeg /tmp/%s_temp.avi''' %
                        (settings.MENCODER_PATH, rotate_nb, filename, filename)))
        logger.info(commands.getoutput('rm /tmp/%s_temp.avi %s' % (filename, filepath)))
        _move_video("/tmp/%s.avi" % filename, filename)
    else:
        _move_video(filepath, filename)

@task
def html5_videos_convert(fileext, filename):
    logger = html5_videos_convert.get_logger()
    logger.info("html5_videos_convert called for %s (extension %s)" % (filename, fileext))
    track = Track.objects.get(original_track=filename)
    _convert(track, fileext, logger)


#@periodic_task(run_every=crontab(hour="*", minute="*", day_of_week="*"))
#def convert_webm():
    #_convert_video("webm")


#@periodic_task(run_every=crontab(hour="*", minute="*", day_of_week="*"))
#def convert_ogg():
    #_convert_video("ogv")


    #* * * * * /var/lib/django/piano-maestoso/cron/send_mail.sh
    #* * * * * /var/lib/django/piano-maestoso/cron/emit_notices.sh

    #0,20,40 * * * * /var/lib/django/piano-maestoso/cron/retry_deferred.sh
