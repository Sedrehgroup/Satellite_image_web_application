from django_celery_beat.models import PeriodicTask , CrontabSchedule , IntervalSchedule


# inter , _ = IntervalSchedule.objects.update_or_create(every=10, period=IntervalSchedule.SECONDS)
at_3_am , _ = CrontabSchedule.objects.get_or_create(minute="0", hour="3", day_of_week="*", day_of_month="*", month_of_year="*",)

PeriodicTask.objects.update_or_create(
    name='delete_images',
    defaults = {
        'crontab' : at_3_am,
        'task' : 'apis.tasks.delete_images'
    }
)