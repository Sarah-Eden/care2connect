from rest_framework import viewsets, serializers
from rest_framework.permissions import IsAuthenticated
from .models import User, Case, Child, FosterFamily, FosterPlacement, HealthService, ReminderLog 
from .serializers import UserSerializer, CaseSerializer, ChildSerializer, FosterFamilySerializer, FosterPlacementSerializer, HealthServiceSerializer, ReminderSerializer
from .permissions import SupervisorGroupPermissions, CaseworkerGroupPermissions, FosterParentGroupPermission

class UserViewSet(viewsets.ModelViewSet):
	queryset = User.objects.all()
	serializer_class = UserSerializer
	permission_class = [SupervisorGroupPermissions]

class CaseViewSet(viewsets.ModelViewSet):
	queryset = Case.objects.all()
	serializer_class = CaseSerializer
	permission_classes = [SupervisorGroupPermissions, CaseworkerGroupPermissions]

class ChildViewSet(viewsets.ModelViewSet):
	queryset = Child.objects.all()
	serializer_class = ChildSerializer
	permission_classes = [SupervisorGroupPermissions, CaseworkerGroupPermissions, FosterParentGroupPermission]

class FosterFamilyViewSet(viewsets.ModelViewSet):
	queryset = FosterFamily.objects.all()
	serializer_class = FosterFamilySerializer
	permission_classes = [SupervisorGroupPermissions]

class FosterPlacementViewSet(viewsets.ModelViewSet):
	queryset = FosterPlacement.objects.all()
	serializer_class = FosterFamilySerializer
	permission_classes = [SupervisorGroupPermissions, CaseworkerGroupPermissions]

class HealthServiceViewSet(viewsets.ModelViewSet):
	queryset = HealthService.objects.all()
	serializer_class = HealthServiceSerializer
	permission_classes = [SupervisorGroupPermissions, CaseworkerGroupPermissions, FosterParentGroupPermission]

class ReminderLogViewSet(viewsets.ModelViewSet):
	queryset = ReminderLog.objects.all()
	serializer_class = ReminderSerializer
	permission_classes = [SupervisorGroupPermissions, CaseworkerGroupPermissions, FosterParentGroupPermission]
