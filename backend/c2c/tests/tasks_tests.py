from django.test import TestCase
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User, Group
from datetime import datetime
from dateutil.relativedelta import relativedelta
from unittest.mock import patch, MagicMock
from c2c.tasks import generate_upcoming_health_services, send_health_reminders
from c2c.models import *
from c2c.constants import EPSDT_REQUIREMENTS

class TasksTestCase(TestCase):
	def setUp(self):
		# User groups
		self.caseworker_group, _ = Group.objects.get_or_create(name='Caseworker')
		self.fosterparent_group, _ = Group.objects.get_or_create(name='FosterParent')

		# New caseworker
		self.caseworker_user = User.objects.create_user(
			username='caseworker1', password='testpass123', email='caseworker1@mail.com',
			first_name='Jill', last_name='Jones', is_active=True
		)
		self.caseworker_user.groups.add(self.caseworker_group)

		# Foster Parents 
		self.fosterparent1_user = User.objects.create_user(
			username='fosterparent1', password='testpass123', email='fp1@mail.com',
			first_name='Sam', last_name='Smith', is_active=True
		)
		self.fosterparent1_user.groups.add(self.fosterparent_group)

		self.fosterparent2_user = User.objects.create_user(
			username='fosterparent2', password='testpass123', email='fp2@mail.com', 
			first_name='Susan', last_name='Smith', is_active=True
		)
		self.fosterparent2_user.groups.add(self.fosterparent_group)

		# Foster Family with 2 parents
		self.family = FosterFamily.objects.create(family_name='2ParentFamily', parent1=self.fosterparent1_user, parent2=self.fosterparent2_user)

		# Create child using fixed birthday to repeat results
		self.child = Child.objects.create(
			first_name='Test', last_name='Child', dob=datetime(2025, 8, 27).date()
		)

		# Create placement
		self.placement = FosterPlacement.objects.create(child=self.child, foster_family=self.family, start_date = datetime(2025, 9, 15).date())

		# Create case, also generating HealthService records due within a 90 day window starting today
		self.case = Case.objects.create_case(child=self.child, caseworker=self.caseworker_user, placement=self.placement, status='open', start_date=datetime(2025, 9, 15).date())

	# Test new record creation on an inappropriate day
	@patch('c2c.tasks.timezone.now')
	def test_generate_upcoming_health_services(self, mock_now):
		# September 25 should not generate new records (will be 4m on 12/27)
		fixed_date = datetime(2025, 9, 25)
		mock_now.return_value = fixed_date

		# Verify HealthService visits at 1 and 2 months exist 
		initial = HealthService.objects.filter(child=self.child)
		initial_count = HealthService.objects.filter(child=self.child).count()
		print(f'DOB: {self.child.dob}, Current Date: {fixed_date.date()}, Age_months: {calculate_age_in_months(self.child.dob, fixed_date.date())}')
		for item in initial:
			print(item)
		self.assertGreater(initial_count, 0, 'No HealthService records created from create_case.')

		# Run task, expect 0 new results.
		result = generate_upcoming_health_services()
		print(f'Test 1 Result: {result}')
		self.assertEqual(HealthService.objects.filter(child=self.child).count(), initial_count, 'New records created inappropriately')

	# Test new record creation on a day that should add a HealthService record for the 4 month visit
	@patch('c2c.tasks.timezone.now')
	def test_generate_upcoming_health_services_on_oct1(self, mock_now):
		fixed_date = datetime(2025, 10, 1)
		mock_now.return_value = fixed_date

	# Verify HealthService visit at 1 and 2 months exist
		initial_count = HealthService.objects.filter(child=self.child).count()
		self.assertGreater(initial_count, 0, 'No HealthService records created from create_case.')

		# Run task, expect 1 new results.
		result = generate_upcoming_health_services()
		print(f'Test 2 Result: {result}')
		record = HealthService.objects.filter(child=self.child)
		for item in record:
			print(item)
		self.assertGreater(HealthService.objects.filter(child=self.child).count(), initial_count, 'HealthService record not created for 4m visit')
	
	# Test email reminder sending
	@patch('c2c.tasks.send_mail')
	def test_send_health_reminders(self, mock_send_mail):
		# Use current date (Sept 30, 2025)
		today = timezone.now().date()
		due_date = today + timedelta(days=30)  # Due Oct 30, 2025, triggers 30-day reminder today
		service = HealthService.objects.create(
			child=self.child,  # Use the child from the case
			service=['well_child'],
			due_date=due_date,
			status='pending'
		)

		result = send_health_reminders()

		# Assert email sent
		# mock_send_mail.assert_called_once()
		logs = ReminderLog.objects.filter(service=service)
		self.assertTrue(logs.exists(), 'No sent logs created')
		self.assertEqual(ReminderLog.objects.filter(service=service).count(), 3, "Unexpected number of logs generated")
		
	def tearDown(self):
		User.objects.all().delete()
		Group.objects.all().delete()
		Child.objects.all().delete()
		FosterFamily.objects.all().delete()
		FosterPlacement.objects.all().delete()
		Case.objects.all().delete()
		HealthService.objects.all().delete()
		ImmunizationRecord.objects.all().delete()
		ReminderLog.objects.all().delete()