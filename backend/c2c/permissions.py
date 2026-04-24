from rest_framework.permissions import DjangoModelPermissions
from .models import Child, Case, FosterFamily, FosterPlacement, HealthService, ImmunizationRecord, ReminderLog
from django.contrib.auth.models import User
from .mixins import get_user_role, get_accessible_child_ids


class RoleBasedPermission(DjangoModelPermissions):
	perms_map = {
		'GET': ['%(app_label)s.view_%(model_name)s'],
		'OPTIONS': [],
		'HEAD': [],
		'POST': ['%(app_label)s.add_%(model_name)s'],
		'PUT': ['%(app_label)s.change_%(model_name)s'],
		'PATCH': ['%(app_label)s.change_%(model_name)s'],
		'DELETE': ['%(app_label)s.delete_%(model_name)s'],
	}
	
	def has_object_permission(self, request, view, obj):
		role = get_user_role(request.user)

		if role == 'Supervisor':
			return True
		if role not in ('Caseworker', 'FosterParent'):
			return False

		child_ids = get_accessible_child_ids(request.user)

		if isinstance(obj, Child):
			return obj.id in child_ids
		if isinstance(obj, (Case, HealthService, ImmunizationRecord, FosterPlacement)):
			return obj.child_id in child_ids
		if isinstance(obj, ReminderLog):
			return obj.service and obj.service.child_id in child_ids
		
		if isinstance(obj, FosterFamily):
			if role == 'Caseworker':
				return True
			return obj.parent1 == request.user or obj.parent2 == request.user
		
		if isinstance(obj, User):
			if role == 'Caseworker':
				return True
			if role == 'FosterParent':
				return Case.objects.filter(
					child_id__in=child_ids, caseworker=obj, status='open'
				).exists()
		
		
		return False