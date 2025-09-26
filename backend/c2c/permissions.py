from rest_framework.permissions import BasePermission, SAFE_METHODS
from django.contrib.auth.models import Group
from django.db.models import Q
from .models import Child, Case, FosterPlacement, HealthService, ImmunizationRecord, ReminderLog
from .utils import get_accessible_case_ids, get_accessible_child_ids

class SupervisorPermissions(BasePermission):
	# Full access to users in the Supervisors group
	def has_permission(self, request, view):
		return request.user.groups.filter(name='Supervisor').exists()
	
	def has_object_permission(self, request, view, obj):
		return self.has_permission(request, view)
	
class CaseworkerPermissions(BasePermission):
	# Limits access to assigned cases and related data
	def has_permission(self, request, view):
		return request.user.groups.filter(name='Caseworker').exists()
	
	def has_object_permission(self, request, view, obj):
		user = request.user
		if not self.has_permission(request, view): 
			return False
		# Get list of cases assigned to caseworker
		accessible_case_ids = get_accessible_case_ids(user)

		if isinstance(obj, Case):
			return obj.id in accessible_case_ids
		
		if isinstance(obj, HealthService):
			if obj.child:
				return Case.objects.filter(id__in=accessible_case_ids, child=obj.child).exists()
			return False
		
		if isinstance(obj, FosterPlacement):
			return Case.objects.filter(id__in=accessible_case_ids, placement=obj).exists()
		
		if isinstance(obj, ImmunizationRecord):
			if obj.child:
				return Case.objects.filter(id__in=accessible_case_ids, child=obj.child).exists()
		
		if isinstance(obj, ReminderLog):
			if obj.service and obj.service.child:
				return Case.objects.filter(id__in=accessible_case_ids, child=obj.service.child).exists()
			return False
		
		# Default to safe methods
		return request.method in SAFE_METHODS

class FosterParentPermissions(BasePermission):
	def has_permission(self, request, view):
		return request.user.groups.filter(name='FosterParent').exists()
	
	def has_object_permission(self, request, view, obj):
		user = request.user

		if not self.has_permission(request, view):
			return False
		
		# Query all active placements for the FosterParent user
		accessible_child_ids = get_accessible_child_ids(user)

		if not accessible_child_ids:
			return False
		
		if isinstance(obj, Child):
			return obj.id in accessible_child_ids
		
		if isinstance(obj, Case):
			if obj.child.id in accessible_child_ids:
				return request.method in SAFE_METHODS
			return False
		
		if isinstance(obj, HealthService):
			return obj.child.id in accessible_child_ids
		
		if isinstance(obj, ImmunizationRecord):
			return obj.child.id in accessible_child_ids
				
		if isinstance(obj, ReminderLog):
			if obj.service.child.id in accessible_child_ids:
				return request.method in SAFE_METHODS
			return False
		# Default to no access
		return False