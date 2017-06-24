from django.test import Client
from unittest import TestCase

from django.urls import reverse

from parser.models import Link, Document
from parser.tests.factories import LinkFactory, DocumentFactory


class TestViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.link1 = LinkFactory.create()
        self.link2 = LinkFactory.create(url='http://linkedin.com/')
        self.document = DocumentFactory.create()
        for link in [self.link1, self.link2]:
            self.document.link.add(link)

    def test_getting_all_documents(self):
        response = self.client.get(reverse('parser:documents'))
        document_from_remote = response.json()['documents'][0]

        self.assertEqual(response.status_code, 200)
        self.assertEqual(document_from_remote['link__count'], Link.objects.all().count())
        self.assertEqual(document_from_remote['id'], Document.objects.last().id)
        self.assertEqual(document_from_remote['name'], Document.objects.last().name)

    def test_getting_links(self):
        response = self.client.get(reverse('parser:links'))
        links_from_remote = response.json()['links']
        urls_from_db = Link.objects.all().values_list('url', flat=True)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(links_from_remote), Link.objects.all().count())
        for link_from_remote in links_from_remote:
            self.assertTrue(link_from_remote['url'] in urls_from_db)

    def test_getting_links_by_document_id(self):
        response = self.client.get(reverse('parser:document', args=(self.document.id,)))
        document_urls = response.json()['urls']
        urls_from_db = Link.objects.all().values_list('url', flat=True)

        self.assertEqual(response.status_code, 200)
        for url in document_urls:
            self.assertTrue(url in urls_from_db)
