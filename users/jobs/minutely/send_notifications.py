import jdatetime
from django.db.models import Q
from django_extensions.management.jobs import BaseJob, MinutelyJob

from users.models import Notification


class Job(MinutelyJob):
    help = "Send scheduled notifications"

    def execute(self):
        date_filter = Q(send_date__lte=jdatetime.date.today())
        time_filter = Q(send_time__lte=jdatetime.datetime.now().time())

        notifications = Notification.objects.filter(
            Q(
                Q(
                    send_date__lte=jdatetime.date.today()
                ) | Q(
                    send_date=jdatetime.date.today(),
                    send_time__lte=jdatetime.datetime.now().time()
                )
            ),
            has_schedule=True,
            is_sent=False,

        ).all()

        for notification in notifications:
            notification.create_user_notifications()
