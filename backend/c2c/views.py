from rest_framework import viewsets, serializers
from rest_framework.permissions import IsAuthenticated
from .models import User, Case, Child, FosterFamily, FosterPlacement, HealthService, ReminderLog 
from .serializers import UserSerializer, CaseSerializer, ChildSerializer, FosterFamilySerializer, FosterPlacementSerializer, HealthServiceSerializer, ReminderSerializer
from .permissions import SupervisorGroupPermissions, CaseworkerGroupPermissions, FosterParentGroupPermission
from .utils import get_accessible_case_ids, get_accessible_child_ids

class UserViewSet(viewsets.ModelViewSet):
	queryset = User.objects.all()
	serializer_class = UserSerializer
	permission_classes = [SupervisorGroupPermissions]

class CaseViewSet(viewsets.ModelViewSet):
	queryset = Case.objects.all()
	serializer_class = CaseSerializer
	permission_classes = [SupervisorGroupPermissions, CaseworkerGroupPermissions]

	def get_queryset(self):
		user = self.request.user
		if user.groups.filter(name='Caseworker').exists():
			return Case.objects.filter(id__in=get_accessible_case_ids(user))
		return Case.objects.all()

class ChildViewSet(viewsets.ModelViewSet):
	queryset = Child.objects.all()
	serializer_class = ChildSerializer
	permission_classes = [SupervisorGroupPermissions, CaseworkerGroupPermissions, FosterParentGroupPermission]

	def get_queryset(self):
		user = self.request.user()
		if user.groups.filter(name='FosterParent').exists():
			return Child.objects.filter(id__in=get_accessible_child_ids(user))
		return Child.object.all()


class FosterFamilyViewSet(viewsets.ModelViewSet):
	queryset = FosterFamily.objects.all()
	serializer_class = FosterFamilySerializer
	permission_classes = [SupervisorGroupPermissions]

class FosterPlacementViewSet(viewsets.ModelViewSet):
	queryset = FosterPlacement.objects.all()
	serializer_class = FosterPlacementSerializer
	permission_classes = [SupervisorGroupPermissions, CaseworkerGroupPermissions]

	def get_queryset(self):
		user=self.request.user
		if user.groups.filter(name='Caseworker').exists():
			return FosterPlacement.objects.filter(case__id__in=get_accessible_case_ids(user), case__status='open')
		return FosterPlacement.objects.all()

class HealthServiceViewSet(viewsets.ModelViewSet):
	queryset = HealthService.objects.all()
	serializer_class = HealthServiceSerializer
	permission_classes = [SupervisorGroupPermissions, CaseworkerGroupPermissions, FosterParentGroupPermission]

	def get_queryset(self):
		user=self.request.user
		if user.groups.filter(name='Caseworker').exists():
			return HealthService.objects.filter(child__case__id__in=get_accessible_case_ids(user), child__case__status='open')
		elif user.groups.filter(name='FosterParent').exists():
			return HealthService.objects.filter(child__id__in=get_accessible_child_ids(user))
		return HealthService.objects.all()

class ReminderLogViewSet(viewsets.ModelViewSet):
	queryset = ReminderLog.objects.all()
	serializer_class = ReminderSerializer
	permission_classes = [SupervisorGroupPermissions, CaseworkerGroupPermissions, FosterParentGroupPermission]

	def get_queryset(self):
		user=self.request.user
		if user.groups.filter(name='Caseworker').exists():
			return ReminderLog.objects.filter(service__child__case__id__in=get_accessible_case_ids(user))
		elif user.groups.filter(name='FosterPrent').exists():
			return ReminderLog.objects.filter(service__child__id__in=get_accessible_child_ids(user))
		return ReminderLog.objects.all()
