#from python
import re 

# from django
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.contrib.auth.models import User

# from pinax
from microblogging.models import Tweet
from pinax.apps.tribes.models import Tribe
from bookmarks.models import Bookmark
from pinax.apps.blog.models import Post


_inbox_count_sources = None
RE_BROWSER = re.compile(r'Firefox/(\d)')


def inbox_count_sources():
    global _inbox_count_sources
    if _inbox_count_sources is None:
        sources = []
        for path in settings.COMBINED_INBOX_COUNT_SOURCES:
            i = path.rfind('.')
            module, attr = path[:i], path[i+1:]
            try:
                mod = __import__(module, {}, {}, [attr])
            except ImportError, e:
                raise ImproperlyConfigured('Error importing request processor module %s: "%s"' % (module, e))
            try:
                func = getattr(mod, attr)
            except AttributeError:
                raise ImproperlyConfigured('Module "%s" does not define a "%s" callable request processor' % (module, attr))
            sources.append(func)
        _inbox_count_sources = tuple(sources)
    return _inbox_count_sources


def combined_inbox_count(request):
    """
    A context processor that uses other context processors defined in
    setting.COMBINED_INBOX_COUNT_SOURCES to return the combined number from
    arbitrary counter sources.
    """
    count = 0
    for func in inbox_count_sources():
        counts = func(request)
        if counts:
            for value in counts.itervalues():
                try:
                    count = count + int(value)
                except (TypeError, ValueError):
                    pass
    return {
        "combined_inbox_count": count,
    }


def footer(request):
    return {
        "latest_tweets": Tweet.objects.all().order_by("-sent")[:5],
        "latest_tribes": Tribe.objects.all().order_by("-created")[:5],
        "latest_users": User.objects.all().order_by("-date_joined")[:9],
        "latest_bookmarks": Bookmark.objects.all().order_by("-added")[:5],
        "latest_blogs": Post.objects.filter(status=2).order_by("-publish")[:5],
    }


def svg_proc(request):
    """ Send a png image if the browser doesn't support css background
    property with svg """
    user_agent = RE_BROWSER.search(request.META['HTTP_USER_AGENT'])
    svg_background = True
    if user_agent:
        svg_background = not int(user_agent.group(1)) < 4
    return {
        "svg_background": svg_background
    }
