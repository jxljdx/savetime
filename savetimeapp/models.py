# -*- coding: utf-8 -*-
from django.db import models
from django.utils import timezone

# Create your models here.

class Category(models.Model):
    """A category a save time item belongs to"""
    CRITICAL = 'critical'
    MAJOR = 'major'
    MINOR = 'minor'
    MAIN_CATEGORY_CHOICES = (
        (CRITICAL, u"极痛"),
        (MAJOR, u"很痛"),
        (MINOR, u"痛")
    )
    main_category = models.CharField(choices=MAIN_CATEGORY_CHOICES, max_length=20, default=CRITICAL)
    sub_category = models.CharField(max_length=128, unique=True)
    num_clicks = models.IntegerField(default=0)
    def __unicode__(self):
        return u'%s' % (self.sub_category)

class Item(models.Model):
    """A save time item which contains basic info like title, link to the site
       detailing about the item, etc.
    """
    title = models.CharField(max_length=200, unique=True)
    created_at = models.DateTimeField(default=timezone.now())
    num_likes = models.IntegerField(default=0)
    url = models.CharField(max_length=300)
    desc = models.CharField(max_length=2048)
    keywords = models.CharField(max_length=200, default='')
    categories = models.ManyToManyField(Category)   # Each save time item can
                                                    # have multiple categories.
    def __unicode__(self):
        return u'%s' % (self.title)

    def category_names(self):
        return ", ".join([c.sub_category for c in self.categories.all()])