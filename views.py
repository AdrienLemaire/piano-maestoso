#from python
import re

# from django
from django.shortcuts import render_to_response
from django.template import RequestContext

RE_BROWSER = re.compile(r'Firefox/(\d)')


def home(request):
    """ Send a png image if the browser doesn't support css background
    property with svg """
    extra_context = {'svg_background' : not int(RE_BROWSER.search(request.META['HTTP_USER_AGENT']).group(1)) < 4}
    return render_to_response("homepage.html", extra_context,
                              context_instance=RequestContext(request))
