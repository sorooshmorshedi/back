from rest_framework import serializers
from rest_framework.exceptions import ErrorDetail
from django.utils.translation import ugettext_lazy as _


def validate_required_fields(attrs, required_fields):
    for field in required_fields:
        if not attrs.get(field):
            error_body = {field: [ErrorDetail(_("This field is required."), code="required")]}
            raise serializers.ValidationError(error_body)
