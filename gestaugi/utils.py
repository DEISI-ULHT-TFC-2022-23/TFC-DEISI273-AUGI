from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa

def save2pdf(template_src, file_name, context_dict={}):
    template = get_template('gestaugi/'+template_src)
    html = template.render(context_dict)
    response = HttpResponse(content_type='application/pdf')
    pdf_status = pisa.CreatePDF(html, dest=response)
    response['Content-Disposition'] = f'attachment; filename=' + file_name

    if pdf_status.err:
        return HttpResponse('Erros <pre>' + html + '</pre>')

    return response