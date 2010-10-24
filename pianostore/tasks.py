# -*- coding:Utf-8 -*-

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


#def _convert_video(type_video):
    #log_file = os.path.join(settings.LOG_DIR, "convert_%s.log" % type_video)
    #logging.basicConfig(filename=log_file,level=logging.DEBUG)
    #for track in Track.objects.all():
        #if not track.__getattribute__("track_%s" % type_video):
            #logging.debug("_convert(%s, %s) ..." % (track, type_video))
            #_convert(track, type_video)
        #else:
            #logging.debug("%s not converted" % track)

def _move_video(path, filename, logger):
    logger.info("shutil.move(%s, os.path.join(%s, %s))" % (path, settings.UPLOAD_DIR, filename))
    shutil.move(path, os.path.join(settings.UPLOAD_DIR, filename))

#@periodic_task(run_every=crontab(hour="*", minute="*", day_of_week="*"))
#def convert_mp4():
    #_convert_video("mp4")

@task
def rotate_video(filepath, original_name, filename, angle):
    logger = rotate_video.get_logger()
    angleToNb = {
        "90" : "1",
        "270" : "2",
    }
    current_ext = original_name.split(".")[-1]
    if angle and angle in angleToNb.keys():
        rotate_nb = angleToNb[angle]
        commands.getoutput('%s -i %s -sameq /tmp/%s_temp.avi' %
            (settings.FFMPEG_PATH, filepath, filename))
        commands.getoutput('%s -vf rotate=%s -o /tmp/%s.avi -oac copy -ovc lavc -lavcopts vcodec=mjpeg /tmp/%s_temp.avi' %
                        (settings.MENCODER_PATH, rotate_nb, filename, filename))
        logger.info("************************** MENCODER END")
        logger.info(commands.getoutput('rm /tmp/%s_temp.avi %s' % (filename, filepath)))
        _move_video("/tmp/%s.avi" % filename, "%s.avi" % filename, logger)
        current_ext = "avi"
    else:
        _move_video(filepath, "%s.%s" % (filename, current_ext), logger)
    track = Track.objects.get(id=int(filename))
    track.original_track = os.path.join(settings.UPLOAD_URL, "%s.%s" % (filename, current_ext))
    track.save()


@task
def html5_videos_convert(fileext, filename):
    logger = html5_videos_convert.get_logger()
    logger.info("html5_videos_convert called for %s (extension %s)" % (filename, fileext))
    logger.info("********************* Track.objects.get(original_track=%s)" % filename)
    track = Track.objects.get(id=int(filename))
    logger.info("track: %s" % track)
    _convert(track, fileext, logger)


#@periodic_task(run_every=crontab(hour="*", minute="*", day_of_week="*"))
#def send_mail():
    #logger = send_mail.get_logger()
    #logger.info(commands.getoutput("%s/cron/send_mail.sh" % settings.PROJECT_ROOT))


#@periodic_task(run_every=crontab(hour="*", minute="*", day_of_week="*"))
#def emit_notices():
    #logger = emit_notices.get_logger()
    #logger.info(commands.getoutput("%s/cron/emit_notices.sh" % settings.PROJECT_ROOT))

#@periodic_task(run_every=crontab(hour="*", minute="*", day_of_week="*"))
#def convert_ogg():
    #_convert_video("ogv")


    #* * * * * /var/lib/django/piano-maestoso/cron/send_mail.sh
    #* * * * * /var/lib/django/piano-maestoso/cron/emit_notices.sh

    #0,20,40 * * * * /var/lib/django/piano-maestoso/cron/retry_deferred.sh
