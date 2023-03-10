from rest_framework import serializers

from reports.models import ExportVerifier


class ExportVerifierSerializer(serializers.ModelSerializer):

    class Meta:
        model = ExportVerifier
        read_only_fields = ('id', )
        exclude = ('financial_year', )
