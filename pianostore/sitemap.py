from django.contrib.sitemaps import Sitemap
from pianostore.models import Track

class TrackSitemap(Sitemap):
    changefreq = "never"
    priority = 1.0

    def items(self):
        return Track.objects.all()

    def lastmod(self, obj):
        return obj.added
