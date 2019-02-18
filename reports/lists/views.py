from io import BytesIO

from django.http import HttpResponse
from django.shortcuts import render
from django.template import Context
from django.template import loader
from django.template.loader import get_template
from rest_framework import generics
from rest_framework.pagination import LimitOffsetPagination
# from weasyprint import HTML
from wkhtmltopdf.views import PDFTemplateView
from xhtml2pdf import pisa

from factors.serializers import ReceiptSerializer
from reports.lists.filters import *
from reports.lists.serializers import *
from sanads.transactions.models import Transaction
from server import settings


class TestView(PDFTemplateView):
    filename = 'my_pdf.pdf'
    template_name = 'reports/sanads.html'
    cmd_options = {
        'margin-top': 3,
        'footer-center': '[page]/[topage]'
    }

    queryset = Sanad.objects.order_by('code')

    def get_context_data(self, **kwargs):
        context = super(TestView, self).get_context_data(**kwargs)
        context['sanads'] = self.queryset
        return context

    def get(self, request):
        pdf = request.GET.get('pdf', None)
        if pdf:
            return super(TestView, self).get(request)
        else:
            return render(request, self.template_name, context={'sanads': self.queryset})


def link_callback(uri, rel):
    import os
    """
    Convert HTML URIs to absolute system paths so xhtml2pdf can access those
    resources
    """
    # use short variable names
    sUrl = settings.STATIC_URL      # Typically /static/
    sRoot = settings.STATIC_ROOT    # Typically /home/userX/project_static/
    mUrl = settings.MEDIA_URL       # Typically /static/media/
    mRoot = settings.MEDIA_ROOT     # Typically /home/userX/project_static/media/

    # convert URIs to absolute system paths
    if uri.startswith(mUrl):
        path = os.path.join(mRoot, uri.replace(mUrl, ""))
    elif uri.startswith(sUrl):
        path = os.path.join(sRoot, uri.replace(sUrl, ""))
    else:
        return uri  # handle absolute uri (ie: http://some.tld/foo.png)

    # make sure that file exists
    if not os.path.isfile(path):
            raise Exception(
                'media URI must start with %s or %s' % (sUrl, mUrl)
            )
    return path


class TransactionListView(generics.ListAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionListSerializer
    filterset_class = TransactionFilter
    ordering_fields = '__all__'
    pagination_class = LimitOffsetPagination


class ChequeListView(generics.ListAPIView):
    queryset = Cheque.objects.all()
    serializer_class = ChequeListSerializer
    filterset_class = ChequeFilter
    ordering_fields = '__all__'
    pagination_class = LimitOffsetPagination


class ChequebookListView(generics.ListAPIView):
    queryset = Chequebook.objects.all()
    serializer_class = ChequebookListSerializer
    filterset_class = ChequebookFilter
    ordering_fields = '__all__'
    pagination_class = LimitOffsetPagination


class SanadListView(generics.ListAPIView):
    queryset = Sanad.objects.all()
    serializer_class = SanadSerializer
    filterset_class = SanadFilter
    ordering_fields = '__all__'
    pagination_class = LimitOffsetPagination
    template = 'reports/sanads.html'

    def get(self, request, *args, **kwargs):
        pdf = request.GET.get('pdf', None)
        if pdf:
            # return render(request, self.template)

            template = get_template(self.template)
            html = template.render()
            response = BytesIO()
            pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), response)
            if not pdf.err:
                return HttpResponse(response.getvalue(), content_type='application/pdf')
            else:
                return HttpResponse("Error Rendering PDF", status=400)

            # html_template = get_template(self.template)
            # pdf_file = HTML(string=html_template).write_pdf()
            # response = HttpResponse(pdf_file, content_type='application/pdf')
            # response['Content-Disposition'] = 'filename="home_page.pdf"'
            # return response

            pass
        else:
            return super(SanadListView, self).get(request, *args, **kwargs)


class FactorListView(generics.ListAPIView):
    queryset = Factor.objects.all()
    serializer_class = FactorListSerializer
    filterset_class = FactorFilter
    ordering_fields = '__all__'
    pagination_class = LimitOffsetPagination


class ReceiptListView(generics.ListAPIView):
    queryset = Receipt.objects.all()
    serializer_class = ReceiptSerializer
    filterset_class = ReceiptFilter
    ordering_fields = '__all__'
    pagination_class = LimitOffsetPagination
