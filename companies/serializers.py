from rest_framework import serializers

from companies.models import Company


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ('id',
                  'name',
                  'fiscal_year_start',
                  'fiscal_year_end',
                  'address1',
                  'address2',
                  'country',
                  'sabt_number',
                  'phone1',
                  'phone2',
                  'fax',
                  'email',
                  'website',
                  'postal_code',
                  'eghtesadi_code',
                  'shenase'
                  )

