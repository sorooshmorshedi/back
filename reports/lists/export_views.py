from django.shortcuts import render
from wkhtmltopdf.views import PDFTemplateView

from companies.models import Company
from factors.models import Factor
from sanads.sanads.models import Sanad


class BaseExportView(PDFTemplateView):
    # filename = 'my_pdf.pdf'
    # template_name = 'reports/sanads.html'
    # queryset = Sanad.objects.order_by('code')
    # context = (
    #     ('form_name', 'سند حسابداری'),
    # )
    cmd_options = {
        'margin-top': 3,
        'footer-center': '[page]/[topage]'
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        company = Company.objects.first()
        context['forms'] = self.queryset
        context['company'] = company
        context['financial_year'] = company.get_financial_year()
        for t in self.context:
            context[t[0]] = t[1]
        return context

    def get(self, request):
        pdf = request.GET.get('pdf', None)
        if pdf:
            return super().get(request)
        else:
            return render(request, self.template_name, context=self.get_context_data())


class SanadExportView(BaseExportView):
    # filename = 'اسناد حساب داری.pdf'
    filename = 'documents.pdf'
    template_name = 'reports/sanads.html'
    queryset = Sanad.objects.order_by('code')
    context = (
        ('form_name', 'سند حسابداری'),
    )


# class FactorExportView(BaseExportView):
#     filename = 'factors.pdf'
#     template_name = 'reports/factors.html'
#     queryset = Factor.objects.order_by('sanad__code')
#     context = ()

