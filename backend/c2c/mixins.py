from rest_framework.viewsets import ViewSetMixin
from django.contrib.auth.models import User
from .models import Case, Child, FosterPlacement, HealthService, ImmunizationRecord, ReminderLog
from .utils import get_accessible_case_ids, get_accessible_child_ids, get_accessible_placement_ids

# Mixin to filter querysets based on user role. Permissions are checked by RoleBasedObject permissions
class RoleBasedQuerySetMixin(ViewSetMixin):

	def get_queryset(self):
		user = self.request.user
		model=self.model or self.queryset.model

		if not user.is_authenticated:
			return model.objects.none()
		
		user_groups = list(user.groups.values_list('name', flat=True))

		# Supervisors view all
		if 'Supervisor' in user_groups:
			return model.objects.all()
		
		if 'Caseworker' in user_groups:
			return self._get_caseworker_queryset(user, model)
		
		if 'FosterParent' in user_groups:
			return self._get_foster_parent_queryset(user, model)
		
		return model.objects.none()
	
	def _get_caseworker_queryset(self, user, model):
		accessible_case_ids = get_accessible_case_ids(user)
		accessible_child_ids = get_accessible_child_ids(user)
		accessible_placement_ids = get_accessible_placement_ids(user)

		if not accessible_case_ids and model != Child:
			return model.objects.none()
		
		if model == Child or model == User:
			return model.objects.all()
		# Map models to their filtering logic
		filters = {
			Case: {'id__in': accessible_case_ids},
			FosterPlacement: {'id__in': accessible_placement_ids},
			HealthService: {'child_id__in': accessible_child_ids},
			ImmunizationRecord: {'child_id__in':accessible_child_ids},
			ReminderLog: {'service__child_id__in': accessible_child_ids},
		}

		filter_kwargs = filters.get(model)
		return model.objects.filter(**filter_kwargs) if filter_kwargs else model.objects.none()
	
	def _get_foster_parent_queryset(self, user, model):
		accessible_child_ids=get_accessible_child_ids(user)

		if not accessible_child_ids:
			return model.objects.none()
		
		# Map models to filtering logic
		filters = {
			Child: {'id__in': accessible_child_ids},
			Case: {'child_id__in': accessible_child_ids},
			HealthService: {'child_id__in': accessible_child_ids},
			ImmunizationRecord: {'child_id__in': accessible_child_ids},
			ReminderLog: {'service__child_id__in': accessible_child_ids},
		}

		filter_kwargs = filters.get(model)
		return model.objects.filter(**filter_kwargs).distinct() if filter_kwargs else model.objects.none()