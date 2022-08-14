def is_shenase_meli(input_code):
    code = str(input_code)
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
    return numbers_sum == control_number
