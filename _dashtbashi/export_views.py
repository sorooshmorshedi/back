import functools
import json

from _dashtbashi.report_views import LadingsReportView
from helpers.exports import get_xlsx_response
from reports.lists.export_views import BaseExportView

title = "لیست بارگیری ها"


def rgetattr(obj, attr, *args):
    def _getattr(obj, attr):
        if hasattr(obj, attr):
            return getattr(obj, attr, *args)
        else:
            return None

    return functools.reduce(_getattr, [obj] + attr.split('.'))


class LadingReportExportView(LadingsReportView, BaseExportView):
    filename = 'ladings'
    template_name = 'reports/lading.html'
    pagination_class = None

    def get_queryset(self):
        return self.filterset_class(self.request.GET, queryset=super().get_queryset()).qs

    def get_context_data(self, user, print_document=False, **kwargs):
        return {}

    def get(self, request, export_type, *args, **kwargs):
        headers = request.GET.get('headers', "[]")
        headers = json.loads(headers)
        return get_xlsx_response('ladings.xlsx', self.get_xlsx_data(self.get_queryset().all(), headers))

    @staticmethod
    def get_xlsx_data(items, headers):
        data = [
            [title],
            ['#'] + [header['text'] for header in headers]
        ]
        i = 0
        for item in items.all():
            i += 1
            row = [i]
            for header in headers:
                row.append(
                    rgetattr(item, header['value'])
                )
            data.append(row)

        return data
