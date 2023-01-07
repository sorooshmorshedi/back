
from django.core.management import call_command
from django.core.management.base import BaseCommand

from companies.models import Company
from payroll.models import WorkshopTax, WorkshopTaxRow


class Command(BaseCommand):
    help = 'load moaf tax table for every company'

    def handle(self, *args, **options):
        companies = Company.objects.all()
        for company in companies:
            tax = WorkshopTax.objects.create(
                company=company,
                name='system_default',
                from_date='1400-01-01',
                to_date='1403-01-01',
                is_verified=True
            )
            WorkshopTaxRow.objects.create(
                workshop_tax=tax,
                from_amount=0,
                to_amount=672000000,
                ratio=0,
            )
            WorkshopTaxRow.objects.create(
                workshop_tax=tax,
                from_amount=672000001,
                to_amount=1800000000,
                ratio=10,
            )
            WorkshopTaxRow.objects.create(
                workshop_tax=tax,
                from_amount=1800000001,
                to_amount=3000000000,
                ratio=15,
            )
            WorkshopTaxRow.objects.create(
                workshop_tax=tax,
                from_amount=3000000001,
                to_amount=4200000000,
                ratio=20,
            )
