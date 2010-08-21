#!/usr/bin/python
# -*- coding:Utf-8 -*-

'''
File: models.py
Author: Adrien Lemaire
Description: Models for the piano app
'''

#python
from os import path
import datetime

# django
from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

# from apps
from photologue.models import Photo
try:
    """ attempt to load the django-tagging TagField from default location,
    otherwise we substitude a dummy TagField. """
    from tagging.fields import TagField
    tagfield_help_text = 'Separate tags with spaces, put quotes around multiple-word tags.'
except ImportError:
    class TagField(models.CharField):
        def __init__(self, **kwargs):
            default_kwargs = {'max_length': 255, 'blank': True}
            default_kwargs.update(kwargs)
            super(TagField, self).__init__(**default_kwargs)
        def get_internal_type(self):
            return 'CharField'
    tagfield_help_text = 'Django-tagging was not found, tags will be treated as plain text.'



#class TrackManager(models.Manager):
    #"""" The track can be a video (various formats) or a audio file. """


class Track(models.Model):
    """Track Model"""
    original_track = models.FileField(_('original track'), upload_to='pianostore/uploads/')
    track_mp4 = models.FileField(_('track.mp4'), upload_to='pianostore/mp4/')
    track_webm = models.FileField(_('track.webm'), upload_to='pianostore/webm/')
    track_ogv = models.FileField(_('track.ogv'), upload_to='pianostore/ogv/')

    title = models.CharField(_('title'), max_length=255)
    title_slug = models.SlugField('slug', unique=True,
        help_text=_('A "slug" is a unique URL-friendly title for an object.'))
    description = models.TextField(_('description'), blank=True)

    artist = models.CharField(_('artist'), max_length=255)
    composer = models.CharField(_('composer'), max_length=255)
    adder = models.ForeignKey(User, related_name="added_tracks",
                              verbose_name=_('adder'))
    is_public = models.BooleanField('is public', default=True,
        help_text=_('Public videos will be displayed in the default views.'))
    date_added = models.DateTimeField(_('added'), default=datetime.datetime.now)

    category = models.CharField(_('category'), max_length=255)
    tags = TagField(help_text=tagfield_help_text, verbose_name=_('tags'))
    image = models.ForeignKey(Photo, blank=True, null=True)

    def get_absolute_url(self):
        return ("describe_track", [self.pk])
    get_absolute_url = models.permalink(get_absolute_url)

    def __unicode__(self):
        return self.title

    def __str__(self):
        return self.__unicode__()

    class Meta:
        ordering = ('-date_added', )
        get_latest_by = 'date_added'
        verbose_name = "track"
        verbose_name_plural = "tracks"

    def save(self, force_insert=False, force_update=False):
        super(Track, self).save(force_insert, force_update)
        if settings.DEBUG:
            try:
                ping_google()
            except Exception:
                pass

    def fullpicture(self):
        """ Get full picture <a>. """
        if self.image:
            link = "%s" % self.image.image.url
            return '<img src=%s />' % (link)
    fullpicture.allow_tags = True

    def _get_thumb_url(self, folder, size):
        """ get a thumbnail giver a folder and a size. """
        if not self.image:
            return
        upload_to = path.dirname(self.image.image.path)
        tiny = path.join(upload_to, folder, path.basename(self.image.image.path))
        tiny = path.normpath(tiny)
        if not path.exists(tiny):
            import Image
            im = Image.open(self.image.image.path)
            im.thumbnail(size, Image.ANTIALIAS)
            im.save(tiny, 'JPEG')
        return path.join(path.dirname(self.image.image.url), folder,
                         path.basename(self.image.image.path)).replace('\\', '/')

    def get_thumb_url(self):
        return self._get_thumb_url('thumb_100_100', (100, 100))

    def thumb(self):
        """ Get thumb <a>. """
        link = self.get_thumb_url()
        if link:
            return '<img src=%s />' % (link)
    thumb.allow_tags = True
