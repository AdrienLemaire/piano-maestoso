import os
import django.core.handlers.wsgi
import sys
from django.conf import settings

logfile = open(settings.PROJECT_ROOT + "/tmp/path.log", "a")
for path in sys.path:
    logfile.write(path + "\n")
logfile.close()
os.environ['DJANGO_SETTINGS_MODULE'] = 'piano-maestoso.settings'

sys.path.insert(0, os.path.join(settings.PROJECT_ROOT, "apps"))

application = django.core.handlers.wsgi.WSGIHandler()

