from django.core.exceptions import ValidationError


def is_shenase_meli(input_code):
    code = str(input_code)
    if len(code) != 11:
        raise ValidationError("َشناسه ملی باید یازده رقم باشد")
    control_number = int(code[10])
    tens_digit_plus_two = int(code[9]) + 2
    tens_coefficients = (29, 27, 23, 19, 17)
    numbers_sum = 0
    i = 0
    while i < 10:
        my_index = i % 5
        numbers_sum += (tens_digit_plus_two + int(code[i])) * tens_coefficients[my_index]
        i += 1
    numbers_sum = numbers_sum % 11
    if numbers_sum == 10:
        numbers_sum = 0
    if numbers_sum != control_number:
        raise ValidationError("َشناسه ملی وارد شده صحیح نیست")
