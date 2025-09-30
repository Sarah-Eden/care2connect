from django_q.tasks import async_task, schedule
from django.utils import timezone
from dateutil.relativedelta import relativedelta
from datetime import timedelta
from django.core.mail import send_mail
from django.conf import settings
from .models import Case, HealthService, ReminderLog, calculate_age_in_months, ImmunizationRecord
from .constants import EPSDT_REQUIREMENTS
import logging

logger = logging.getLogger(__name__)
# Monthly task: Generate new HealthService records due in the next 60-90 day for all active cases.
def generate_upcoming_health_services():
	today = timezone.now().date()
	window_end = today + timedelta(days=90)
	active_cases = Case.objects.filter(status='open')
	new_wc_count = 0
	new_dental_count = 0

	for case in active_cases:
		child = case.child
		current_age_months = calculate_age_in_months(child.dob, today)
		age_in_3months = current_age_months + 3
		due_date_offset = 10 if current_age_months < 31 else 30

		# Well child visits
		services_by_date = {}

		for age in EPSDT_REQUIREMENTS['well_child_schedule']['age_in_months']:
			if current_age_months < age <= age_in_3months:
				due_date = child.dob + relativedelta(months=age) + timedelta(days=due_date_offset)
				services_by_date[due_date] = {
					'age_months': age,
					'services': ['well_child'],
					'immunizations': []
				}
		
		# Immunizations 
		for date, data in services_by_date.items():
			age = data['age_months']

			for vaccine, vaccine_data in EPSDT_REQUIREMENTS['immunization_schedule'].items():
				for dose_info in vaccine_data:
					if 'age_months' in dose_info and 'dose' in dose_info:
						dose_ages = dose_info['age_months'] if isinstance(dose_info['age_months'], list) else [dose_info['age_months']]
						if age in dose_ages:
							if not ImmunizationRecord.objects.filter(
								child=child,
								vaccine_name=vaccine,
								dose_number=int(dose_info['dose'][0]),
							).exists():
								data['immunizations'].append(vaccine)

		# Create HealthService records for well child/immunization visits
		for date, data in services_by_date.items():
			if not HealthService.objects.filter(child=child, service__contains='well_child', due_date=date):
				new_service = HealthService.objects.create(
					child = child,
					service = data['services'],
					immunizations = data['immunizations'],
					due_date = date,
					status='pending' 
				)
				new_wc_count += 1

		# Add dental checup if child > 12 months of age
		if current_age_months >= 12:
			new_service = HealthService.objects.create(
				child=child,
				service=['dental'],
				due_date = timezone.now().date() + timedelta(days=30),
				status='pending'
			)
			new_dental_count +=1
		
	return f'Created {new_wc_count} new well_child and {new_dental_count} new dental HealthService records.'

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
			if case.caseworker.email:
				recipients.append(case.caseworker)
			if case.placement.foster_family:
				family = case.placement.foster_family
				if family.parent1.email:
					recipients.append(family.parent1)
				if family.parent2.email:
					recipients.append(family.parent2)

			for person in recipients:
				print(f'Service: {service.id}, Recipient: {person.email}')
			if not recipients:
				continue

			subject = f'Health Service Reminder'
			message = f'Health Service Reminder for {case.child.first_name} {case.child.last_name}. The {', '.join(service.service)} is due in {interval} days on {service.due_date}.'

			try:
				for person in recipients:
					send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, person.email, fail_silently=False)
					ReminderLog.objects.create(
						user = person,
						service = service,
						sent_date = today,
						status = 'sent'
					)
					sent_count += 1
			except Exception as e:
				ReminderLog.objects.create(
					user = person,
					service = service,
					sent_date = today,
					status = 'failed'
				)
				failed_count += 1
				print(f'Email failed for service {service.id}: {str(e)}')
	return f'Sent {sent_count} reminders, {failed_count} failures'
