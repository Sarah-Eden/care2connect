from django.db.models import Q
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from .models import FosterPlacement, Case

def get_accessible_child_ids(user):
	if user.groups.filter(name='Caseworker').exists():
		active_cases = Case.objects.filter(caseworker=user, status='open')
		child_ids = {case.child_id for case in active_cases if case.child_id}
		return child_ids
	
	if user.groups.filter(name='FosterParent').exists():
		active_placements = FosterPlacement.objects.filter(
			(Q(foster_family__parent1=user) | Q(foster_family__parent2=user)) & Q(end_date__isnull=True))
		child_ids = set(active_placements.values_list('child_id', flat=True))
		return child_ids

	return set()

def get_accessible_case_ids(user):
	if user.groups.filter(name='Caseworker').exists():
		active_cases = Case.objects.filter(caseworker=user, status='open')
		case_ids = set(active_cases.values_list('id', flat=True))
		return case_ids
	return set()

def get_accessible_placement_ids(user):
	if user.groups.filter(name='Caseworker').exists():
		active_cases = Case.objects.filter(caseworker=user, status='open')
		placement_ids = {case.placement_id for case in active_cases if case.placement_id}
		return placement_ids
	return set()