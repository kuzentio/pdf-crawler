from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST

from .models import Document, Link
from .utils import convert_pdf_to_txt, get_urls_from_text, require_pdf_file


@require_GET
def get_documents(request):
    documents = Document.objects.values(
        'id', 'name'
    ).annotate(
        Count('link')
    )
    data = {
        'documents': list(documents)
    }

    return JsonResponse(data)


@require_GET
def get_document(request, document_id):
    document = get_object_or_404(
        Document, pk=document_id
    )
    urls = Link.objects.filter(
        document=document
    ).values(
        'url'
    )
    data = {
        'urls': list(urls)
    }

    return JsonResponse(data)


@require_GET
def get_links(request):
    links = Link.objects.prefetch_related(
        'documents'
    ).values(
        'id', 'url'
    ).annotate(
        Count('documents')
    )
    data = {
        'links': list(links)
    }

    return JsonResponse(data)


@csrf_exempt
@require_POST
@require_pdf_file
def upload_document(request, document_name, file):
    text = convert_pdf_to_txt(file)
    urls = get_urls_from_text(text)

    for url in urls:
        link, _ = Link.objects.get_or_create(
            url=url
        )
        document, _ = Document.objects.get_or_create(
            name=document_name,
        )
        document.link.add(link)

    return JsonResponse({'success': True})
