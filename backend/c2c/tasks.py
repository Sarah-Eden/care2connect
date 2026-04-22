from django_q.tasks import async_task, schedule
from django.utils import timezone
from dateutil.relativedelta import relativedelta
from datetime import timedelta
from django.core.mail import send_mail
from django.conf import settings
from .models import Case, HealthService, ReminderLog, generate_health_services
import logging

logger = logging.getLogger(__name__)
# Monthly task: Generate new HealthService records due in the next 60-90 day for all active cases.
def generate_upcoming_health_services():
	today = timezone.now().date()
	active_cases = Case.objects.filter(status='open')
	total_wc = 0
	total_dental = 0

	for case in active_cases:
		wc, dental = generate_health_services(case.child, today)
		total_wc += wc
		total_dental += dental
		
	return f'Created {total_wc} new well_child and {total_dental} new dental HealthService records.'

# Daily task: Send email reminders for HealthService records due in 30, 14, and 7 days. Logs sends/failures
def send_health_reminders():
	today = timezone.now().date()
	intervals = [30, 14, 7]
	sent_count = 0
	failed_count = 0

	for interval in intervals:
		target_date = today + timedelta(days=interval)
		services = HealthService.objects.filter(
			status = 'pending',
			due_date = target_date
		)
	
		for service in services:
			case = service.child.cases.filter(status='open').first()
			logger.debug(f'Service: {service.due_date}, Case: {case}, Status: {case.status if case else None}')
			if not case:
				continue

			recipients = []
			if case.caseworker:
				recipients.append(case.caseworker)
			if case.placement and case.placement.foster_family:
				family = case.placement.foster_family
				if family.parent1:
					recipients.append(family.parent1)
				if family.parent2:
					recipients.append(family.parent2)

			if not recipients:
				continue

			subject = f'Health Service Reminder'
			message = f'Health Service Reminder for {case.child.first_name} {case.child.last_name}. The {", ".join(service.service)} is due in {interval} days on {service.due_date}.'

			try:
				for person in recipients:
					send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, person.email, fail_silently=False)
					ReminderLog.objects.create(
						user = person,
						service = service,
						sent_date = timezone.now(),
						status = 'sent'
					)
					sent_count += 1
			except Exception as e:
				ReminderLog.objects.create(
					user = person,
					service = service,
					sent_date = timezone.now(),
					status = 'failed'
				)
				failed_count += 1
				logger.error(f'Email failed for service {service.id}: {str(e)}')
	return f'Sent {sent_count} reminders, {failed_count} failures'
