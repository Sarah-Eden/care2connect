from django.db.models import Q
from django.utils import timezone
from .models import FosterPlacement, Case

def get_accessible_child_ids(user):
	if user.groups.filter(name='FosterParent').exists():
		active_placements = FosterPlacement.objects.filter((Q(foster_family__parent1=user) | Q(foster_family__parent2=user)) & Q(end_date__isnull=True))
		return set(active_placements.values_list('child_id', flat=True))
	return set()

def get_accessible_case_ids(user):
	if user.groups.filter(name='Caseworker').exists():
		active_cases = Case.objects.filter(caseworker=user, status='open')
		return set(active_cases.values_list('id', flat=True))
	return set()