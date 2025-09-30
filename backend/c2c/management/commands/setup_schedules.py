from django.core.management.base import BaseCommand
from django_q.tasks import schedule
from django_q.models import Schedule

class Command(BaseCommand):
	help = 'Set up Djanog-Q2 schedules for tasks'

	def handle(self, *args, **options):
		# Monthly health service record creation (midnight on day 1)
		schedule(
			func= 'c2c.tasks.generate_upcoming_health_services',
			name= 'monthly_healthservice_record_generator',
			schedule_type = Schedule.CRON,
			cron='0 0 1 * *'	# 12am on day 1 of the month
		)

		# Daily email reminders
		schedule(
			func = 'c2c.tasks.send_health_reminders',
			name = 'daily_health_reminders',
			schedule_type = Schedule.CRON,
			cron = '0 0 * * *' # Every day at 12am
		)

		print(self.style.SUCCESS('Schedules setup successfully'))
		