from django.core.management.base import BaseCommand

from payroll.models import WorkTitle


class Command(BaseCommand):
    help = 'load fixtures'

    def handle(self, *args, **options):
        for title in WorkTitle.objects.all():
            title.delete()
