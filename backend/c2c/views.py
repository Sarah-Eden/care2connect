from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import User, Case, Child, FosterFamily, FosterPlacement, HealthService, ReminderLog, ImmunizationRecord 
from .serializers import UserSerializer, CaseSerializer, ChildSerializer, FosterFamilySerializer, FosterPlacementSerializer, HealthServiceSerializer, ReminderSerializer, ImmunizationRecordSerializer
from .permissions import RoleBasedObjectPermissions
from .mixins import RoleBasedQuerySetMixin

# Create your views here.		
class UserViewSet(RoleBasedQuerySetMixin, viewsets.ModelViewSet):
	queryset = User.objects.all()
	serializer_class = UserSerializer
	model = User
	permission_classes = [IsAuthenticated, RoleBasedObjectPermissions]

	def get_queryset(self):
		queryset = super().get_queryset()

		# Filter users by group
		group_name = self.request.query_params.get('group', None)
		if group_name:
			queryset = queryset.filter(groups__name=group_name).distinct()
		
		return queryset

class CaseViewSet(RoleBasedQuerySetMixin, viewsets.ModelViewSet):
	queryset = Case.objects.all()
	serializer_class = CaseSerializer
	model = Case
	permission_classes = [IsAuthenticated, RoleBasedObjectPermissions]

class ChildViewSet(RoleBasedQuerySetMixin, viewsets.ModelViewSet):
	queryset = Child.objects.all()
	serializer_class = ChildSerializer
	model = Child
	permission_classes = [IsAuthenticated, RoleBasedObjectPermissions]
	
class FosterFamilyViewSet(RoleBasedQuerySetMixin, viewsets.ModelViewSet):
	queryset = FosterFamily.objects.all()
	serializer_class = FosterFamilySerializer
	model = FosterFamily
	permission_classes = [IsAuthenticated, RoleBasedObjectPermissions]

class FosterPlacementViewSet(RoleBasedQuerySetMixin, viewsets.ModelViewSet):
	queryset = FosterPlacement.objects.all()
	serializer_class = FosterPlacementSerializer
	model = FosterPlacement
	permission_classes = [IsAuthenticated, RoleBasedObjectPermissions]

class HealthServiceViewSet(RoleBasedQuerySetMixin, viewsets.ModelViewSet):
	queryset = HealthService.objects.all()
	serializer_class = HealthServiceSerializer
	model = HealthService
	permission_classes = [IsAuthenticated, RoleBasedObjectPermissions]

class ReminderLogViewSet(RoleBasedQuerySetMixin, viewsets.ModelViewSet):
	queryset = ReminderLog.objects.all()
	serializer_class = ReminderSerializer
	model = ReminderLog
	permission_classes = [IsAuthenticated, RoleBasedObjectPermissions]

class ImmunizationRecordViewset(RoleBasedQuerySetMixin, viewsets.ModelViewSet):
	queryset = ImmunizationRecord
	serializer_class = ImmunizationRecordSerializer
	model = ImmunizationRecord
	permission_classes = [IsAuthenticated, RoleBasedObjectPermissions]
