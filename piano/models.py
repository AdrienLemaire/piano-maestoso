#!/usr/bin/python
# -*- coding:Utf-8 -*-

'''
File: models.py
Author: Adrien Lemaire
Description: Models for the piano app
'''

#python
from datetime import datetime

# django
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User


class Track(models.Model):
    """Track Model"""
    title = models.CharField(_('title'), max_length=255)
    artist = models.CharField(_('artist'), max_length=255)
    composer = models.CharField(_('artist'), max_length=255)
    category = models.CharField(_('artist'), max_length=255)
    description = models.TextField(_('description'), blank=True)
    adder = models.ForeignKey(User, related_name="added_books",
                              verbose_name=_('adder'))
    added = models.DateTimeField(_('added'), default=datetime.now)

    class Meta:
        ordering = ('-added', )
