import os
import django.core.handlers.wsgi
import sys
logfile = open("/home/fandekasp/piano-maestoso/tmp/path.log", "a")
for path in sys.path:
    logfile.write(path + "\n")
logfile.close()
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

from django.conf import settings
sys.path.insert(0, os.path.join(settings.PROJECT_ROOT, "apps"))

application = django.core.handlers.wsgi.WSGIHandler()

