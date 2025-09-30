from django.test import TestCase
from django.contrib.auth.models import User, Group
from django.utils import timezone
from c2c.models import Case, Child, FosterFamily, FosterPlacement, HealthService, ImmunizationRecord
from datetime import timedelta
from dateutil.relativedelta import relativedelta

class EPSDTTestCase(TestCase):
	# Taken from auth_tests.py for consistency
	def setUp(self):
		# Dynamically get or create role groups
		self.supervisor_group, _ = Group.objects.get_or_create(name='Supervisor')
		self.caseworker_group, _ = Group.objects.get_or_create(name='Caseworker')
		self.fosterparent_group, _ = Group.objects.get_or_create(name='FosterParent')

		 # Create test users
		self.supervisor_user = User.objects.create_user(
			username='supervisor1', password='testpass123', email='supervisor1@mail.com',
			first_name='Jane', last_name='Doe', is_active=True
		)
		self.supervisor_user.groups.add(self.supervisor_group)

		self.caseworker_user = User.objects.create_user(
			username='caseworker1', password='testpass123', email='caseworker1@mail.com',
			first_name='Jill', last_name='Jones', is_active=True
		)
		self.caseworker_user.groups.add(self.caseworker_group)

		self.fosterparent1_user = User.objects.create_user(
			username='fosterparent1', password='testpass123', email='fp1@mail.com',
			first_name='Sam', last_name='Smith', is_active=True
		)
		self.fosterparent1_user.groups.add(self.fosterparent_group)

		# Create default data (taken from auth_tests.py)
		self.family = FosterFamily.objects.create(family_name='TestFamily', parent1=self.fosterparent1_user)
		# Child dob modified to test automatic HealthService record generation
		self.child = Child.objects.create(first_name='Test', last_name='Child', dob=timezone.now().date() - relativedelta(months=1))
		self.placement = FosterPlacement.objects.create(child=self.child, foster_family=self.family, start_date=timezone.now().date())
		self.case = Case.objects.create_case(
            child=self.child, caseworker=self.caseworker_user, placement=self.placement,
            status='open', start_date=timezone.now().date()
        )
		# Create immunization records for HepB dose at birth
		self.immunization1 = ImmunizationRecord.objects.create(
			child=self.child,
			vaccine_name = 'HepB,',
			dose_number = 1,
			total_doses = 3,
			date_administered = self.child.dob	
		)

		self.immunization2 = ImmunizationRecord.objects.create(
			child=self.child,
			vaccine_name='DTaP', 
			dose_number=1,
			total_doses = 5,
			date_administered=None
		)
	
	def test_initial_health_service_creation(self):
		case = Case.objects.create_case(
			child=self.child,
			caseworker = self.caseworker_user,
			placement= self.placement,
			status='open', 
			start_date=timezone.now().date()
		)

		# Verify HealthService records are created
		health_services = HealthService.objects.filter(child=case.child)
		self.assertGreater(len(health_services), 0, 'No HealthService records created')

		# Check for well-child visit (should be 10 days after 2 month milestone)
		child = case.child
		wc_due = child.dob + relativedelta(months=2) + timedelta(days=10)
		wc_service = health_services.filter(service__contains='well_child', due_date=wc_due).first()
		self.assertIsNotNone(wc_service, 'Well-child service not created')
		self.assertEqual(wc_service.status, 'pending')
		self.assertIn('well_child', wc_service.service)

		# Check for dental, should fail as child < 12 months old
		dental_service = health_services.filter(service__contains='dental').first()
		self.assertIsNone(dental_service, 'Dental service created for child < 12 months')
	
	def test_health_service_creation_for_toddler(self):
		toddler = Child.objects.create(
			first_name = 'Toddler',
			last_name = 'Child',
			dob = timezone.now().date() - relativedelta(months=35)
		)

		toddler_placement = FosterPlacement.objects.create(
			child=toddler,
			foster_family = self.family,
			start_date=timezone.now().date()
		)

		toddler_case = Case.objects.create_case(
			child=toddler,
			caseworker = self.caseworker_user,
			placement=toddler_placement,
			status='open',
			start_date=timezone.now().date()
		)

		# Verify HealthService records, should be a visit at 30 days past 36 months
		health_services = HealthService.objects.filter(child=toddler)
		self.assertGreater(len(health_services), 0, 'No HealthService records exist')
		service_due = toddler.dob + relativedelta(months=36) + relativedelta(days=30)
		toddler_wc_service = health_services.filter(service__contains='well_child', due_date=service_due).first()
		self.assertIsNotNone(toddler_wc_service, 'Well-child service not created')
		self.assertEqual(toddler_wc_service.status, 'pending')
		self.assertIn('well_child', toddler_wc_service.service)


	def tearDown(self):  
		User.objects.all().delete()
		Child.objects.all().delete()
		FosterFamily.objects.all().delete()
		FosterPlacement.objects.all().delete()
		Case.objects.all().delete()
		HealthService.objects.all().delete()
		ImmunizationRecord.objects.all().delete()
		Group.objects.all().delete() 