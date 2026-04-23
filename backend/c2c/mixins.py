from rest_framework.viewsets import ViewSetMixin
from django.db.models import Q
from django.contrib.auth.models import User
from .models import Case, Child, FosterFamily, FosterPlacement, HealthService, ImmunizationRecord, ReminderLog


def get_accessible_child_ids(user):
	if user.groups.filter(name='Caseworker').exists():
		return set(
			Case.objects.filter(caseworker=user, status='open').values_list('child_id', flat=True)
		)
	if user.groups.filter(name='FosterParent').exists():
		return set(
			FosterPlacement.objects.filter(
				(Q(foster_family__parent1=user) | Q(foster_family__parent2=user)),
				end_date__isnull=True
			).values_list('child_id', flat=True)
		)
	return set()

def get_user_role(user):
	groups = set(user.groups.values_list('name', flat=True))

	for role in ('Supervisor', 'Caseworker', 'FosterParent'):
		if role in groups:
			return role
	
	return None


class RoleBasedQuerySetMixin(ViewSetMixin):

	def get_queryset(self):
		user = self.request.user
		model=self.model or self.queryset.model

		if not user.is_authenticated:
			return model.objects.none()
		
		role = get_user_role(user)

		if role == 'Supervisor':
			return model.objects.all()
		if role not in ('Caseworker', 'FosterParent'):
			return model.objects.none()
		
		child_ids = get_accessible_child_ids(user)
		if not child_ids:
			return model.objects.none()
		
		if model == FosterFamily:
			if role == 'Caseworker':
				return model.objects.all()
			return model.objects.filter(Q(parent1=user) | Q(parent2=user)).distinct()
	
		if model == User:
			caseworker_ids = (
				Case.objects.filter(child_id__in=child_ids, status='open').values_list('caseworker_id', flat=True).distinct()
			)
			return model.objects.filter(id__in=caseworker_ids)
		
		filters = {
			Child: {'id__in': child_ids},
			Case: {'child_id__in': child_ids},
			HealthService: {'child_id__in': child_ids},
			ImmunizationRecord: {'child_id__in': child_ids},
			FosterPlacement: {'child_id__in': child_ids},
			ReminderLog: {'service__child_id__in': child_ids},
		}

		filter_kwargs = filters.get(model)
		return model.objects.filter(**filter_kwargs) if filter_kwargs else model.objects.none()
		

	