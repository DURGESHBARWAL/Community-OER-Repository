from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
import xhtml2pdf.pisa as pisa

import os

class Render:

    @staticmethod
    def render(path: str, params: dict, filename, dirname=None):
        template = get_template(path)
        html = template.render(params)
        response = BytesIO()
        if os.path.isdir("Files"):
            result = open("Files/"+filename, 'wb')
        else:
            os.makedirs("Files")
            result = open("Files/"+filename, 'wb')
        pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), response)
        pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
        result.close()
        if not pdf.err:
            return HttpResponse(response.getvalue(), content_type='application/pdf')
        else:
            return HttpResponse("Error Rendering PDF", status=400)


