from django.db import models


class Link(models.Model):
    url = models.URLField(max_length=255)

    def __unicode__(self):
        return self.url


class Document(models.Model):
    name = models.CharField(max_length=255)
    link = models.ManyToManyField(Link, related_name='documents')

    def __unicode__(self):
        return self.name
