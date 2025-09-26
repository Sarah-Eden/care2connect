from django.db.models import Q
import datetime
from .models import FosterPlacement, Case

def calculate_age(date_of_birth):
	today = datetime.datetime.now()
	dob = datetime.datetime.strptime(date_of_birth, '%d/%m/%Y')

	total_days = today - dob
	print(total_days)

	years = (total_days.total_seconds())/(365.25*24*3600)
	yearsInt = int(abs(years))
	
	months = (years - yearsInt)*12
	monthsInt = int(abs(months))

	age_months = (yearsInt * 12) + monthsInt

	return age_months

	
	 


def get_accessible_child_ids(user):
	if user.groups.filter(name='FosterParent').exists():
		active_placements = FosterPlacement.objects.filter(
			(Q(foster_family__parent1=user) | Q(foster_family__parent2=user)) & Q(end_date__isnull=True))
		child_ids = set(active_placements.values_list('child_id', flat=True))
		print(f'get_accessible_child_ids: User {user.username}, Active Placements: {active_placements}')
		return child_ids
	print(f'get_accessible_child_ids: User {user.username} is not a FosterParent, returning empty set')
	return set()

def get_accessible_case_ids(user):
	if user.groups.filter(name='Caseworker').exists():
		active_cases = Case.objects.filter(caseworker=user, status='open')
		case_ids = set(active_cases.values_list('id', flat=True))
		print(f'get_accessible_case_ids: User {user.username}, Active Placements: {active_cases}')
		return case_ids
	print(f'get_accessible_case_ids: User {user.username} is not a Caseworker, returning empty set')
	return set()