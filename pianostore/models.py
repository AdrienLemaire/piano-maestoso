#!/usr/bin/python
# -*- coding:Utf-8 -*-

'''
File: models.py
Author: Adrien Lemaire
Description: Models for the piano app
'''

#python
from os import path
from datetime import datetime

# django
from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User


class Track(models.Model):
    """Track Model"""
    title = models.CharField(_('title'), max_length=255)
    artist = models.CharField(_('artist'), max_length=255)
    composer = models.CharField(_('artist'), max_length=255)
    category = models.CharField(_('artist'), max_length=255)
    coverart = models.ImageField(upload_to="pianostore", blank=True, null=True)
    description = models.TextField(_('description'), blank=True)
    adder = models.ForeignKey(User, related_name="added_tracks",
                              verbose_name=_('adder'))
    added = models.DateTimeField(_('added'), default=datetime.now)

    def get_absolute_url(self):
        return ("describe_track", [self.pk])
    get_absolute_url = models.permalink(get_absolute_url)

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ('-added', )

    def _get_thumb_url(self, folder, size):
        """ get a thumbnail giver a folder and a size. """
        if not self.coverart:
            return '#'
        upload_to = path.dirname(self.coverart.path)
        tiny = path.join(upload_to, folder, path.basename(self.coverart.path))
        tiny = path.normpath(tiny)
        if not path.exists(tiny):
            import Image
            im = Image.open(self.coverart.path)
            im.thumbnail(size, Image.ANTIALIAS)
            im.save(tiny, 'JPEG')
        return path.join(path.dirname(self.coverart.url), folder,
                         path.basename(self.coverart.path)).replace('\\', '/')

    def get_thumb_url(self):
        return self._get_thumb_url('thumb_100_100', (100, 100))

    def thumb(self):
        """ Get thumb <a>. """
        link = self.get_thumb_url()
        if link is None:
            return '<a href="#" target="_blank">NO IMAGE</a>'
        else:
            return '<img src=%s />' % (link)
    thumb.allow_tags = True

    def fullpicture(self):
        """ Get full picture <a>. """
        link = "%s%s" % (settings.MEDIA_URL, self.coverart)
        if link is None:
            return '<a href="#" target="_blank">NO IMAGE</a>'
        else:
            return '<img src=%s />' % (link)
    fullpicture.allow_tags = True
