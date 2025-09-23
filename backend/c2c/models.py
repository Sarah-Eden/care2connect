from django.db import models
from django.contrib.auth.models import User
from multiselectfield import MultiSelectField

class Child(models.Model):
	first_name = models.CharField(max_length=150)
	last_name = models.CharField(max_length=150)
	dob = models.DateField()
	medications = models.TextField(blank=True, null=True)
	allergies = models.TextField(blank=True, null=True)

class FosterFamily(models.Model):
	family_name = models.CharField(max_length=256)
	parent1 = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='parent1')
	parent2 = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='parent2')
	max_occupancy = models.IntegerField(default=1)
	current_occupancy = models.IntegerField(default=0)

class FosterPlacement(models.Model):
	child = models.ForeignKey(Child, on_delete=models.SET_NULL, null=True)
	foster_family = models.ForeignKey(FosterFamily, on_delete=models.SET_NULL, null=True)
	start_date = models.DateField()
	end_date = models.DateField(blank=True)
	end_reason = models.TextField(null=True, blank=True)
	
class Case(models.Model):
	child = models.ForeignKey(Child, on_delete=models.CASCADE)
	caseworker = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
	placement = models.ForeignKey(FosterPlacement, on_delete=models.SET_NULL, null=True)
	start_date = models.DateField()
	end_date = models.DateField(null=True, blank=True)
	status = models.CharField(choices=[('open', 'Open'), ('closed', 'Closed')])

class HealthService(models.Model):
	SERVICE_CHOICES = (
		('well_child', 'Well Child Checkup'),
		('immunization(s)', 'Immunization(s)'),
		('dental', 'Dental'),
		('vision', 'Vision'),
		('hearing', 'Hearing')
	)

	IMMUNIZATION_CHOICES = (
		('rsv', 'Respiratory Syncytial Virus (RSV)'),
		('hepb', 'Hepatitis B'),
		('rv', 'Rotavirus (RV)'),
		('dtap', 'Diptheria, Tetanus & Acellular Pertussis (DTaP)'), 
		('tdap', 'Tetanus, Diptheria, & Acellular Pertussis (TDaP)'),
		('hib', 'Haemophilus Influenzae type b (Hib)'),
		('pcv15', 'Pneumococcal Conjugate (PCV15)'),
		('pcv20', 'Pneumococcal Conjugate (PCV20)'),
		('ipv', 'Inactivated Poliovirus (IPV)'),
		('covid_mrna', 'COVID-19 (1vCOV-mRNA)'),
		('covid_aps', 'COVID-19 (1vCOV-aPS)'),
		('iiv3', 'Influenza'),
		('mmr', 'Measles, Mumps, Rubella'),
		('var', 'Varicella (VAR)'),
		('hepa', 'Hepatitis A (HepA)'),
		('hpv', 'Human Papillomavirus (HPV)'),
		('menacwy-crm', 'Meningococcal (MenACWY-CRM)'),
		('menacwy-tt', 'Meningococcal (Meningococcal (MenACWY-TT))'),
		('dengue', 'Dengue (DEN4CYD)'),
		('mpox', 'Mpox'),
		('none', None)
	)
	
	child = models.ForeignKey(Child, on_delete=models.CASCADE)
	service = MultiSelectField(choices=SERVICE_CHOICES, min_choices=1)
	immunizations = MultiSelectField(choices=IMMUNIZATION_CHOICES, min_choices=1, default=None, null=True)
	due_date = models.DateField()
	completed_date = models.DateField()
	status = models.CharField(choices=[('pending', 'Pending'), ('complete', 'Complete')])
	created_date = models.DateTimeField(auto_now_add=True)
	updated_date = models.DateTimeField(null=True, default=None)

class ReminderLog(models.Model):
	user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
	service = models.ForeignKey(HealthService, on_delete=models.SET_NULL, null=True)
	set_date = models.DateTimeField()
	status = models.CharField(choices=[('sent', 'Sent'), ('failed', 'Failed')])
