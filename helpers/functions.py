def get_current_user():
    from helpers.middlewares.ModifyRequestMiddleware import ModifyRequestMiddleware

    return ModifyRequestMiddleware.user


def get_new_child_code(parent_code, child_code_length, last_child_code=None):
    if last_child_code:
        last_code = int(last_child_code) + 1
        code = str(last_code)
    else:
        last_code = '1'.zfill(child_code_length)
        code = parent_code + last_code

    if code[:len(parent_code)] != parent_code:
        from rest_framework import serializers
        raise serializers.ValidationError("تعداد فرزندان این سطح پر شده است")

    return code


def get_new_code(last_code=None, max_length=None):
    if not last_code:
        return 1
    else:
        code = str(int(last_code) + 1)
        if len(code) > max_length:
            from rest_framework import serializers
            raise serializers.ValidationError("تعداد اعضای این سطح پر شده است")
    return code
