from rest_framework.permissions import BasePermission, SAFE_METHODS
from django.contrib.auth.models import Group
from django.db.models import Q
from .models import Child, Case, FosterPlacement, HealthService, ReminderLog
from .utils import get_accessible_case_ids, get_accessible_child_ids

class SupervisorGroupPermissions(BasePermission):
	# Full access to users in the Supervisors group
	def has_permission(self, request, view): 
		return request.user.is_authenticated and request.user.groups.filter(name='Supervisor').exists()
	
	def has_object_permission(self, request, view, obj):
		return request.user.is_authenticated and request.user.groups.filter(name='Supervisor').exists()
	
class CaseworkerGroupPermissions(BasePermission):
	# Limits access to assigned cases and related data
	def has_permission(self, request, view):
		return request.user.is_authenticated and request.user.groups.filter(name='Caseworker').exists()
	
	def has_object_permission(self, request, view, obj):
		# Get list of cases assigned to caseworker
		accessible_case_ids = get_accessible_case_ids(request.user)

		if not self.has_permission(request, view):
			return False
		if isinstance(obj, Case):
			return obj.id in accessible_case_ids
		elif isinstance(obj, HealthService):
			return Case.objects.filter(id__in=accessible_case_ids, placement=obj, status='open').exists()
		elif isinstance(obj, FosterPlacement):
			return Case.objects.filter(id__in=accessible_case_ids, placement=obj, status='open').exists()
		elif isinstance(obj, ReminderLog):
			if obj.service:
				return Case.objects.filter(id_in=accessible_case_ids, child=obj.service.child, status='open').exists()
		return request.method in SAFE_METHODS

class FosterParentGroupPermission(BasePermission):
	def has_permission(self, request, view):
		return request.user.is_authenticated and request.user.groups.filter(name='FosterParent').exists()
	
	def has_object_permission(self, request, view, obj):
		if not self.has_permission(request, view):
			return False
		
		# Query all active placements for the FosterParent user
		child_in_placement = get_accessible_child_ids(request.user)
		if not child_in_placement:
			return False
		
		if isinstance(obj, Case):
			return obj.child in child_in_placement and request.method in ['GET', 'PUT', 'PATCH']
		if isinstance(obj, Child):
			return obj.id in child_in_placement
		elif isinstance(obj, HealthService):
			return obj.child_id in child_in_placement
		elif isinstance(obj, ReminderLog):
			if obj.service and obj.service.child_id in child_in_placement:
				return True
			return False
		return False

class ReadOnly(BasePermission):
	def has_permission(self, request, view):
		return request.method in SAFE_METHODS
	def has_object_permission(self, request, view, obj):
		return request.method in SAFE_METHODS