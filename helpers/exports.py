from io import BytesIO

import pandas
import xlsxwriter
from django.http.response import HttpResponse


def get_xlsx_response(sheet_name, data):
    with BytesIO() as b:
        writer = pandas.ExcelWriter(b, engine='xlsxwriter')

        df = pandas.DataFrame(data)
        df.to_excel(
            writer,
            sheet_name=sheet_name,
            index=False,
            header=False
        )
        workbook = writer.book
        worksheet = writer.sheets[sheet_name]
        worksheet.right_to_left()

        border_fmt = workbook.add_format({'bottom': 1, 'top': 1, 'left': 1, 'right': 1})
        worksheet.conditional_format(xlsxwriter.utility.xl_range(
            0, 0, len(data) - 1, len(df.columns) - 1
        ), {'type': 'no_errors', 'format': border_fmt})
        writer.save()

        return HttpResponse(b.getvalue(), content_type='application/vnd.ms-excel')
