from factory.django import DjangoModelFactory

from parser.models import Link, Document


class LinkFactory(DjangoModelFactory):
    class Meta:
        model = Link
        django_get_or_create = ('url', )

    url = 'http://google.com/'


class DocumentFactory(DjangoModelFactory):
    class Meta:
        model = Document
        django_get_or_create = ('name', )

    name = 'document'
