from rest_framework.permissions import BasePermission, SAFE_METHODS
from django.contrib.auth.models import Group
from django.db.models import Q
from .models import Child, Case, FosterPlacement, HealthService, ReminderLog

class SupervisorGroupPermissions(BasePermission):
	# Full access to users in the Supervisors group
	def has_permission(self, request, view): 
		return request.user.is_authenticated and request.user.groups.filter(name='Supervisor').exits()
	
	def has_object_permission(self, request, view, obj):
		return request.user.is_authenticated and request.user.groups.filter(name='Supervisors').exists()
	
class CaseworkerGroupPermissions(BasePermission):
	# Limits access to assigned cases and related data
	def has_permission(self, request, view):
		return request.user.is_authenticated and request.user.groups.filter(name='Caseworker').exists()
	
	def has_object_permission(self, request, view, obj):
		if request.user.is_authenticated and request.user.groups.filter(name='Caseworker').exists():
			if isinstance(obj, Case):
				return obj.caseworker==request.user and obj.status=='open'
			elif isinstance(obj, HealthService):
				return Case.objects.filter(caseworker=request.user, child=obj.child, status='open').exists()
			elif isinstance(obj, FosterPlacement):
				return Case.objects.filter(caseworker=request.user, placement=obj, status='open').exists()
			elif isinstance(obj, ReminderLog):
				return HealthService.objects.filter(id=obj.service_id, child__case__caseworker=request.user, child__case__status='open').exists()
			elif isinstance(obj, (Case, HealthService, FosterPlacement)) and not isinstance(obj, ReminderLog):
				return Case.objects.filter(caseworker=request.user, child=obj.child).exists()	
		return False

class FosterParentGroupPermission(BasePermission):
	def has_permission(self, request, view):
		return request.user.is_authenticated and request.user.groups.filter(name='FosterParent').exists()
	
	def has_object_permission(self, request, view, obj):
		if request.user.is_authenticated and request.user.groups.filter(name='FosterParent').exists:
			placement = FosterPlacement.objects.filter(Q(foster_family__parent1=request.user) | Q(foster_family__parent2=request.user)).first()
			if placement:
				if isinstance(obj, Child):
					return obj == placement.child
				elif isinstance(obj, HealthService):
					return obj.child==placement.child
				elif isinstance(obj, ReminderLog):
					return HealthService.objects.filter(id=obj.service_id, child=placement.child).exists()
				elif isinstance(obj, (Case)):
					return obj.child==placement.child

class ReadOnly(BasePermission):
	def has_permission(self, request, view):
		return request.method in SAFE_METHODS
	def has_object_permission(self, request, view, obj):
		return request.method in SAFE_METHODS