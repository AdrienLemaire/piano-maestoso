# from python
import logging
import os

# from project
from celery.decorators import task#periodic_task, task
#from celery.task.schedules import crontab
from settings import LOG_DIR

# from app
from pianostore.management.commands.convert_videos import _convert
from pianostore.models import Track


def _convert_video(type_video):
    log_file = os.path.join(LOG_DIR, "convert_%s.log" % type_video)
    logging.basicConfig(filename=log_file,level=logging.DEBUG)
    for track in Track.objects.all():
        if not track.__getattribute__("track_%s" % type_video):
            logging.debug("_convert(%s, %s) ..." % (track, type_video))
            _convert(track, type_video)
        else:
            logging.debug("%s not converted" % track)


#@periodic_task(run_every=crontab(hour="*", minute="*", day_of_week="*"))
#def convert_mp4():
    #_convert_video("mp4")
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
