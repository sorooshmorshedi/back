from rest_framework import status
from rest_framework.views import exception_handler

labels = {
    # User
    'username': 'نام کاربری',

    # Use full
    'name': 'نام',
    'postal_code': 'کد پستی',
    'mobile': 'موبایل',
    'phone': 'موبایل',
    'account': 'حساب',
    'date': 'تاریخ',
    'type': 'نوع',

    # Cheque
    'serial_from': 'از شماره سریال',
    'serial_to': 'تا شماره سریال',

    # Ware
    'ware': 'کالا',
    'unit': 'واحد شمارش',
    'category': 'دسته بندی',
    'pricingType': 'نوع قیمت گذاری',
    'price': 'قیمت',

    # Other
    'code': 'شماره',
    'form': 'فرم',
    'post': 'سمت',

    # Dashtbashi
    'destination': 'مقصد',
    'origin': 'مبدا',
    'contractor': 'پیمانکار',
    'end_date': 'تاریخ پایان',
    'loading_date': 'تاریخ بارگیری',
    'issue_date': 'تاریخ صدور',
    'remittance_payment_method': 'روش پرداخت مبلغ حواله',
    'driver_tip_payer': 'پرداخت کننده انعام',
    'lading_number': 'شماره بارگیری',
    'billNumber': 'شماره بارنامه',
    'receive_type': 'نحوه دریافت',
    'owner': 'مالک',

}


def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    if response is not None and response.status_code != status.HTTP_500_INTERNAL_SERVER_ERROR:
        errors = []
        data = response.data
        if isinstance(data, list):
            message = data[0]
        else:
            message = data.get('detail')
        if not message:
            for field, value in response.data.items():
                errors.append({
                    'field': labels.get(field, field),
                    'messages': value
                })
        else:
            errors.append({
                'field': '',
                'messages': [message]
            })

        response.data = errors

    return response
