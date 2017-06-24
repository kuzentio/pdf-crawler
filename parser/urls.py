from django.conf.urls import url

from . import views

urlpatterns = [
    url(
        regex=r'^$',
        view=views.get_documents,
        name='documents'
    ),
    url(
        regex=r'^(?P<document_id>\d+)/$',
        view=views.get_document,
        name='document'
    ),
    url(
        regex=r'^links/$',
        view=views.get_links,
        name='links'
    ),
    url(
        regex=r'^upload/$',
        view=views.upload_document,
        name='upload_document'
    ),

]
