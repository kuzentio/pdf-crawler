import re
import json
from StringIO import StringIO

from django.http import HttpResponse

from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage


def convert_pdf_to_txt(file):
    result_str = StringIO()
    converter = TextConverter(rsrcmgr=PDFResourceManager(), outfp=result_str, laparams=LAParams())
    interpreter = PDFPageInterpreter(PDFResourceManager(), converter)

    for page in PDFPage.get_pages(file):
        interpreter.process_page(page)

    text = result_str.getvalue()

    file.close()
    converter.close()
    result_str.close()

    return text


def get_urls_from_text(text):
    urls = re.findall(
        'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',
        text
    )
    return urls


def require_pdf_file(view_func):
    def _wrapped_view_func(request, *args, **kwargs):
        if not request.FILES or len(request.FILES.items()) > 1:
            return json_response_bad_request({'message': 'Bad request, please provide .PDF file.'})
        document_name, file = request.FILES.items()[0]
        if not file.content_type == 'application/pdf':
            return json_response_bad_request({'message': 'Bad request, please provide .PDF file.'})

        return view_func(request, document_name, file, *args, **kwargs)

    return _wrapped_view_func


def json_response_bad_request(vars):
    msg = {
        'status_code': 400,
        'content_type': 'application/json',
    }
    msg.update(vars)
    return HttpResponse(json.dumps(msg), status=400, content_type='applecation/json')
