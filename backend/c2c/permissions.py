from rest_framework.permissions import BasePermission, DjangoModelPermissions, SAFE_METHODS
from django.contrib.auth.models import User
from .models import Child, Case, FosterFamily, FosterPlacement, HealthService, ImmunizationRecord, ReminderLog
from .utils import get_accessible_case_ids, get_accessible_child_ids

class ModelPermissionsWithView(DjangoModelPermissions):
	# Map HTTP methods to Django permission type
	permissions_map = {
		'GET': ['%(app_label)s.view_%(model_name)s'],
		'OPTIONS': [],
		'HEAD': [],
		'POST': ['%(app_label)s.add_%(modelname)s'],
		'PUT': ['%(app_label)s.change_%(modelname)s'],
		'PATCH': ['%(app_label)s.change_%(modelname)s'],
		'DELETE': ['%(app_label)s.delete_%(modelname)s'],
	}

class RoleBasedObjectPermissions(ModelPermissionsWithView):
	
	def has_object_permission(self, request, view, obj):
		user = request.user
		user_groups = list(user.groups.values_list('name', flat=True))		

		if 'Supervisor' in user_groups:
			return True
		
		if 'Caseworker' in user_groups:
			return self._check_caseworker_access(user, obj)
		
		if 'FosterParent' in user_groups: 
			return self._check_foster_parent_access(user, obj, request)
		
		return False
	
	def _check_caseworker_access(self, user, obj):
		# Check if caseworker has access to specific object
		accessible_case_ids = get_accessible_case_ids(user)

		if not accessible_case_ids:
			return False
		
		if isinstance(obj, User):
			return True
		
		if isinstance(obj, Case):
			return obj.id in accessible_case_ids
		
		if isinstance(obj, (HealthService, ImmunizationRecord)):
			return Case.objects.filter(id__in=accessible_case_ids, child=obj.child).exists()
		
		if isinstance(obj, FosterPlacement):
			return Case.objects.filter(id__in=accessible_case_ids, child=obj.child).exists()
		
		if isinstance(obj, FosterFamily):
			return True
		
		if isinstance(obj, ReminderLog):
			if obj.service and obj.service.child:
				return Case.objects.filter(id__in=accessible_case_ids, child=obj.service.child).exists()
			return False
		
		return 
	
	def _check_foster_parent_access(self, user, obj, request):
		accessible_child_ids = get_accessible_child_ids(user)

		if not accessible_child_ids:
			return False
		
		if isinstance(obj, Child):
			return obj.id in accessible_child_ids
		
		if isinstance(obj, (HealthService, ImmunizationRecord)):
			return obj.child.id in accessible_child_ids
		
		if isinstance(obj, Case):
			return obj.child.id in accessible_child_ids and request.method in SAFE_METHODS
		
		if isinstance(obj, FosterPlacement):
			return obj.child in accessible_child_ids and request.method in SAFE_METHODS
		
		if isinstance(obj, FosterFamily):
			return (obj.parent1 == user or obj.parent2 == user) and request.method in SAFE_METHODS
		
		if isinstance(obj, User):
			assigned_caseworker = Case.objects.filter(child_id__in=accessible_child_ids, caseworker=obj, status='open')
			return assigned_caseworker.exists() and request.method in SAFE_METHODS
		
		if isinstance(obj, ReminderLog):
			if obj.service and obj.service.child:
				return obj.service.child.id in accessible_child_ids and request.method in SAFE_METHODS
			return False
		
		return False