#from python
import re

# from django
from django.shortcuts import render_to_response
from django.template import RequestContext

RE_BROWSER = re.compile(r'Firefox/(\d)')


def home(request):
    """ Send a png image if the browser doesn't support css background
    property with svg """
    svg_background = True
    user_agent = RE_BROWSER.search(request.META['HTTP_USER_AGENT'])
    if user_agent:
        svg_background = not int(user_agent.group(1)) < 4
    return render_to_response("homepage.html", {"svg_background": svg_background},
                              context_instance=RequestContext(request))
