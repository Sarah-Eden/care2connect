from django.db import models
from django.contrib.auth.models import User
from django.forms import ValidationError
from multiselectfield import MultiSelectField
from .constants import SERVICE_CHOICES, IMMUNIZATION_CHOICES, IMMUNIZATION_DOSES

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
	
class Case(models.Model):
	child = models.ForeignKey(Child, on_delete=models.CASCADE)
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
