from django.db import models, transaction
from django.db.models import Q, UniqueConstraint
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from multiselectfield import MultiSelectField
from .constants import SERVICE_CHOICES, IMMUNIZATION_CHOICES, IMMUNIZATION_DOSES, EPSDT_REQUIREMENTS
from django.utils import timezone
from datetime import timedelta
from dateutil.relativedelta import relativedelta

class Child(models.Model):
	first_name = models.CharField(max_length=150)
	last_name = models.CharField(max_length=150)
	dob = models.DateField()
	medications = models.TextField(blank=True, null=True)
	allergies = models.TextField(blank=True, null=True)

	class Meta:
		verbose_name_plural = 'children'
		unique_together = ('first_name', 'last_name', 'dob')

	def __str__(self):
		return f'{self.last_name}, {self.first_name}'

class FosterFamily(models.Model):
	family_name = models.CharField(max_length=256)
	parent1 = models.ForeignKey(User, on_delete=models.PROTECT, null=True, related_name='parent1')
	parent2 = models.ForeignKey(User, on_delete=models.PROTECT, null=True, related_name='parent2')
	max_occupancy = models.IntegerField(default=1)
	
	@property
	def current_occupancy(self):
		return FosterPlacement.objects.filter(
			foster_family=self, end_date__isnull=True
		).count()

	class Meta:
		verbose_name_plural = 'FosterFamilies'
		
	def __str__(self):
		return self.family_name

class FosterPlacement(models.Model):
	child = models.ForeignKey(Child, on_delete=models.PROTECT, null=True)
	foster_family = models.ForeignKey(FosterFamily, on_delete=models.PROTECT, null=True)
	start_date = models.DateField()
	end_date = models.DateField(blank=True, null=True)
	end_reason = models.TextField(null=True, blank=True)

	class Meta:
		constraints = [
			UniqueConstraint(
				fields=['child'],
				condition=Q(end_date__isnull=True),
				name='unique_active_placement'
			)
		]

	def __str__(self):
		child_name = self.child.last_name if self.child else 'Unknown'
		family_name = self.foster_family.family_name if self.foster_family else 'Unknown'
		return f'Child Last Name: {child_name}, Foster Family: {family_name}'


def calculate_age_in_months(date_of_birth, reference_date=None):
	if reference_date is None:
		reference_date = timezone.now().date()
	
	if hasattr(date_of_birth, 'date'):
		date_of_birth = date_of_birth.date()
	if hasattr(reference_date, 'date'):
		reference_date = reference_date.date()

	delta_age = relativedelta(reference_date, date_of_birth)

	return delta_age.years * 12 + delta_age.months


def generate_health_services(child, reference_date):
	current_age_months = calculate_age_in_months(child.dob, reference_date)
	age_in_3months = current_age_months + 3
	due_date_offset = 10 if current_age_months < 30 else 30
	wc_count = 0
	dental_count = 0

	services_by_date = {}
	for age in EPSDT_REQUIREMENTS['well_child_schedule']['age_in_months']:
		if current_age_months < age <= age_in_3months:
			due_date = child.dob + relativedelta(months=age) + timedelta(days=due_date_offset)
			services_by_date[due_date] = {
				'age_months': age,
				'services': ['well_child'],
				'immunizations': []
			}

	for date, data in services_by_date.items():
		age = data['age_months']
		for vaccine, vaccine_data in EPSDT_REQUIREMENTS['immunization_schedule'].items():
			for dose_info in vaccine_data.get('schedule', []):
				if 'age_months' in dose_info and 'dose' in dose_info:
					dose_ages = dose_info['age_months'] if isinstance(dose_info['age_months'], list) else [dose_info['age_months']]
					if age in dose_ages:
						if not ImmunizationRecord.objects.filter(
							child=child,
							vaccine_name=vaccine,
							dose_number=int(dose_info['dose'][0]),
						).exists():
							data['immunizations'].append(vaccine)
	
	for date, data in services_by_date.items():
		if not HealthService.objects.filter(child=child, service__contains='well_child', due_date=date).exists():
			HealthService.objects.create(
				child=child,
				service=data['services'],
				immunizations=data['immunizations'],
				due_date=date,
				status='pending'
			)
			wc_count +=1
	
	dental_due = None

	if current_age_months >= 12:
		last_dental = HealthService.objects.filter(
			child=child, service__contains='dental'
		).order_by('-due_date').first()

		if not last_dental:
			dental_due = reference_date + timedelta(days=30)
		else:
			next_dental = last_dental.due_date + timedelta(days=183)
			if next_dental <= reference_date + timedelta(days=90):
				dental_due = next_dental
	
	elif current_age_months < 12 <= age_in_3months:
		dental_due = child.dob + relativedelta(months=12) + timedelta(days=due_date_offset)
		
	if dental_due:
		if not HealthService.objects.filter(
			child=child, service__contains='dental', due_date=dental_due
		).exists():
			HealthService.objects.create(
				child=child,
				service=['dental'],
				due_date=dental_due,
				status='pending'
			)
			dental_count +=1

	return wc_count, dental_count

class CaseManager(models.Manager):
	@transaction.atomic
	def create_case(self, child, caseworker, status, start_date, placement=None, end_date=None):
		case = self.model(
			child=child,
			caseworker=caseworker,
			placement=placement,
			status=status,
			start_date=start_date,
			end_date=end_date
		)
		case.save()
		generate_health_services(child, start_date)
		return case

class Case(models.Model):
	objects = CaseManager()
	child = models.ForeignKey(Child, on_delete=models.PROTECT, related_name='cases')
	caseworker = models.ForeignKey(User, on_delete=models.PROTECT, null=True)
	placement = models.ForeignKey(FosterPlacement, on_delete=models.PROTECT, null=True, blank=True)
	start_date = models.DateField()
	end_date = models.DateField(null=True, blank=True)
	status = models.CharField(choices=[('open', 'Open'), ('closed', 'Closed')], default='open')	

	class Meta:
		constraints=[
			UniqueConstraint(
				fields=['child'],
				condition=Q(status='open'),
				name='unique_open_case'
			)
		]
	
class HealthService(models.Model):	
	child = models.ForeignKey(Child, on_delete=models.CASCADE)
	service = MultiSelectField(choices=SERVICE_CHOICES, min_choices=1)
	immunizations = MultiSelectField(choices=IMMUNIZATION_CHOICES, blank=True, default='')
	due_date = models.DateField()
	completed_date = models.DateField(null=True, blank=True)
	status = models.CharField(choices=[('pending', 'Pending'), ('complete', 'Complete')], default='pending')
	created_date = models.DateTimeField(auto_now_add=True)
	updated_date = models.DateTimeField(auto_now=True)

	def __str__(self):
		return f'{self.service} record for {self.child}, due on {self.due_date}'
	def __repr__(self):
		return f'<HealthService: {self.child.last_name}, {self.service}, {self.immunizations}, {self.due_date}'
	
	def save(self, *args, **kwargs):
		super().save(*args, **kwargs)

		if self.status == 'complete' and self.completed_date:
			for vaccine in self.immunizations or []:
				vaccine_data = EPSDT_REQUIREMENTS['immunization_schedule'].get(vaccine)
				if not vaccine_data:
					continue

				existing = ImmunizationRecord.objects.filter(child=self.child, vaccine_name=vaccine).order_by('-dose_number').first()
				next_dose = (existing.dose_number + 1) if existing else 1
				total = vaccine_data.get('total_doses', 0)
			
				if next_dose > total:
					continue
				
				record, created = ImmunizationRecord.objects.get_or_create(
					child = self.child,
					vaccine_name = vaccine,
					dose_number = next_dose,
					total_doses = total,
					date_administered = self.completed_date
				)


class ImmunizationRecord(models.Model):
	child = models.ForeignKey(Child, on_delete=models.CASCADE)
	vaccine_name = models.CharField(choices=IMMUNIZATION_CHOICES)
	dose_number = models.PositiveSmallIntegerField()
	total_doses = models.PositiveSmallIntegerField(default=0)
	date_administered = models.DateField(null=True, blank=True)

	class Meta:
		unique_together = ('child', 'vaccine_name', 'dose_number')
	
	def clean(self):
		super().clean()

		if self.date_administered and self.dose_number >1:
			prev_dose = ImmunizationRecord.objects.filter(child=self.child, vaccine_name=self.vaccine_name, dose_number=self.dose_number-1).first()
			
			if not prev_dose or not prev_dose.date_administered:
				raise ValidationError(f'Dose #{self.dose_number} requires dose #{self.dose_number-1} to be administered first.')
			if self.dose_number > self.total_doses:
				raise ValidationError(f'Dose number cannot exceed total number required')
	
	def save(self, *args, **kwargs):
		if not self.pk:
			self.total_doses = IMMUNIZATION_DOSES.get(self.vaccine_name, 0)
		self.full_clean()
		super(ImmunizationRecord, self).save(*args, **kwargs)
		
class ReminderLog(models.Model):
	user = models.ForeignKey(User, on_delete=models.PROTECT, null=True)
	service = models.ForeignKey(HealthService, on_delete=models.PROTECT, null=True)
	sent_date = models.DateTimeField()
	status = models.CharField(choices=[('sent', 'Sent'), ('failed', 'Failed')], default='sent')
