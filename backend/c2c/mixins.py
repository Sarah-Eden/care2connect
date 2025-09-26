from django.db.models import Q
from rest_framework.viewsets import ViewSetMixin
from .models import Case, Child, FosterPlacement, HealthService, ImmunizationRecord, ReminderLog
from .utils import get_accessible_case_ids, get_accessible_child_ids

"""
	This mixin handles role based access control queryset filtering for viewsets. It assumes the user's role was
	validated and filters data based on that role.
"""
# Handles RBAC queryset filtering for viewsets
# Assumes permissions have validated the user's role, and filters data based on that role.
class RBACMixin(ViewSetMixin):
	# Model is set by the viewset
	model = None
	def get_queryset(self):
		user = self.request.user
		if not hasattr(user, 'groups'):
			return self.model.objects.none()
		
		if user.groups.filter(name='Supervisor').exists():
			return self.model.objects.all()
		
		if user.groups.filter(name='Caseworker').exists():
			accessible_case_ids = get_accessible_case_ids(user)

			if not accessible_case_ids:
				return self.model.objects.none()
			
			child_ids = Case.objects.filter(id__in=accessible_case_ids).values_list('child_id', flat=True)
			placement_ids = Case.objects.filter(id__in=accessible_case_ids).values_list('placement_id', flat=True)

			if self.model == Case:
				return self.model.objects.filter(id__in=accessible_case_ids)
			elif self.model == Child:
				return self.model.objects.filter(id__in=child_ids)			
			elif self.model == FosterPlacement:
				return self.model.objects.filter(id__in=placement_ids)			
			elif self.model == HealthService:
				return self.model.objects.filter(child_id__in=child_ids)
			elif self.model == ImmunizationRecord:
				return self.model.objects.filter(child_id__in=child_ids)			
			elif self.model == ReminderLog:
				return self.model.objects.filter(service__child_id__in=child_ids)			
			return self.model.objects.none()
		
		if user.groups.filter(name='FosterParent').exists():
			accessible_child_ids = get_accessible_child_ids(user)
			
			if not accessible_child_ids:
				return self.model.objects.none()

			if self.model == Child:
				return self.model.objects.filter(id__in=accessible_child_ids)
			elif self.model == HealthService:
				return self.model.objects.filter(child_id__in=accessible_child_ids)
			elif self.model == ImmunizationRecord:
				return self.model.objects.filter(child_id__in=accessible_child_ids)
			elif self.model == ReminderLog:
				return self.model.objects.filter(service__child_id__in=accessible_child_ids)
			return self.model.objects.none()
		
		return self.model.objects.none()

