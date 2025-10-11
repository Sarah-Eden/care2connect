from django.db import models, transaction
from django.contrib.auth.models import User
from django.forms import ValidationError
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

	def __str__(self):
		return f'{self.last_name}, {self.first_name}'

class FosterFamily(models.Model):
	family_name = models.CharField(max_length=256)
	parent1 = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='parent1')
	parent2 = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='parent2')
	max_occupancy = models.IntegerField(default=1)
	current_occupancy = models.IntegerField(default=0)

	class Meta:
		verbose_name_plural = 'FosterFamilies'
	def __str__(self):
		return self.family_name

class FosterPlacement(models.Model):
	child = models.ForeignKey(Child, on_delete=models.SET_NULL, null=True)
	foster_family = models.ForeignKey(FosterFamily, on_delete=models.SET_NULL, null=True)
	start_date = models.DateField()
	end_date = models.DateField(blank=True, null=True)
	end_reason = models.TextField(null=True, blank=True)

	def __str__(self):
		return f'Child Last Name: {self.child.last_name}, Foster Family: {self.foster_family.family_name}'

def calculate_age_in_months(date_of_birth, reference_date=None):
	if reference_date is None:
		reference_date = timezone.now().date()
	
	if hasattr(date_of_birth, 'date'):
		date_of_birth = date_of_birth.date()
	if hasattr(reference_date, 'date'):
		reference_date = reference_date.date()

	delta_age = relativedelta(reference_date, date_of_birth)

	return delta_age.years * 12 + delta_age.months

class CaseManager(models.Manager):
	@transaction.atomic
	def create_case(self, child, caseworker, status, start_date, placement=None, end_date=None):
		# Create the case instance and generate initial HealthService records
		case = self.model(
			child=child,
			caseworker=caseworker,
			placement=placement,
			status=status,
			start_date=start_date,
			end_date=end_date
		)
		case.save()

		# Create HealthService records for the 3-months following the case start_date
		child = child
		start_date = start_date
		end_date = start_date + timedelta(days=91)

		current_age_months = calculate_age_in_months(child.dob, start_date)
		age_in_3months = current_age_months + 3
		due_date_offset = 10 if current_age_months < 30 else 30

		# Get well child visits in 3 month window
		services_by_date = {}
		for age in EPSDT_REQUIREMENTS['well_child_schedule']['age_in_months']:
			if current_age_months < age <= age_in_3months:
				due_date = child.dob + relativedelta(months=age) + timedelta(days=due_date_offset)
				services_by_date[due_date] = {
					'age_months': age,
					'services': ['well_child'],
					'immunizations': []
				}

		# Get Immunizaation requirements based on well child visits
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
			new_service = HealthService.objects.create(
				child = child,
				service = data['services'],
				immunizations = data['immunizations'],
				due_date = date,
				status='pending' 
			)

		# Add dental checkup if child > 12 months of age
		if current_age_months >= 12:
			new_service = HealthService.objects.create(
				child=child,
				service=['dental'],
				due_date = timezone.now().date() + timedelta(days=30),
				status='pending'
			)
		
		return case

class Case(models.Model):
	objects = CaseManager()
	child = models.ForeignKey(Child, on_delete=models.CASCADE, related_name='cases')
	caseworker = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
	placement = models.ForeignKey(FosterPlacement, on_delete=models.SET_NULL, null=True, blank=True)
	start_date = models.DateField()
	end_date = models.DateField(null=True, blank=True)
	status = models.CharField(choices=[('open', 'Open'), ('closed', 'Closed')])	
	
class HealthService(models.Model):	
	child = models.ForeignKey(Child, on_delete=models.CASCADE)
	service = MultiSelectField(choices=SERVICE_CHOICES, min_choices=1)
	immunizations = MultiSelectField(choices=IMMUNIZATION_CHOICES, default=None, null=True)
	due_date = models.DateField()
	completed_date = models.DateField(null=True, blank=True)
	status = models.CharField(choices=[('pending', 'Pending'), ('complete', 'Complete')])
	created_date = models.DateTimeField(auto_now_add=True)
	updated_date = models.DateTimeField(null=True, blank=True)

	def __str__(self):
		return f'{self.service} record for {self.child}, due on {self.due_date}'
	def __repr__(self):
		return f'<HealthService: {self.child.last_name}, {self.service}, {self.immunizations}, {self.due_date}'
	
	def save(self, *args, **kwargs):
		super().save(*args, **kwargs)

		# Automatically generate ImmunizationRecord instances when HealthService status marked complete
		if self.status == 'complete' and self.completed_date:
			for vaccine in self.immunizations or []:
				vaccine_data = EPSDT_REQUIREMENTS['immunization_schedule'].get(vaccine)
				if not vaccine_data:
					continue

				existing = ImmunizationRecord.objects.filter(child=self.child, vaccine_name=vaccine).order_by('-dose_number').first()
				next_dose = (existing.dose_number + 1) if existing else 1
				total = vaccine_data.get('total_doses', 0)
			
				if next_dose > total:
					break
				
				record, created = ImmunizationRecord.objects.get_or_create(
					child = self.child,
					vaccine_name = vaccine,
					dose_number = next_dose,
					total_doses = total,
					date_administered = self.completed_date
				)

				if not created:
					print(f'Existing record found for {vaccine} dose #{next_dose}. Skipping create')


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
		self.total_doses = IMMUNIZATION_DOSES.get(self.vaccine_name, 0)
		super(ImmunizationRecord, self).save(*args, **kwargs)
		
class ReminderLog(models.Model):
	user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
	service = models.ForeignKey(HealthService, on_delete=models.SET_NULL, null=True)
	sent_date = models.DateTimeField()
	status = models.CharField(choices=[('sent', 'Sent'), ('failed', 'Failed')])
