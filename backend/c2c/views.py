from rest_framework import viewsets, generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import User, Case, Child, FosterFamily, FosterPlacement, HealthService, ReminderLog, ImmunizationRecord 
from .serializers import UserSerializer, CaseSerializer, ChildSerializer, FosterFamilySerializer, FosterPlacementSerializer, HealthServiceSerializer, ReminderSerializer, CustomTokenObtainPairSerializer, ImmunizationRecordSerializer
from .permissions import SupervisorPermissions, CaseworkerPermissions, FosterParentPermissions
from .mixins import RBACMixin
from rest_framework_simplejwt.views import TokenObtainPairView


class CreateUserView(generics.CreateAPIView):
	queryset = User.objects.all()	
	serializer_class = UserSerializer
	permission_classes = [AllowAny]

class CustomTokenObtainPairView(TokenObtainPairView):
	serializer_class = CustomTokenObtainPairSerializer
	
class UserViewSet(RBACMixin, viewsets.ModelViewSet):
	queryset = User.objects.all()
	serializer_class = UserSerializer
	model = User
	permission_classes = [IsAuthenticated, SupervisorPermissions]

class CaseViewSet(RBACMixin, viewsets.ModelViewSet):
	queryset = Case.objects.all()
	serializer_class = CaseSerializer
	model = Case
	permission_classes = [IsAuthenticated, SupervisorPermissions|CaseworkerPermissions]

class ChildViewSet(RBACMixin, viewsets.ModelViewSet):
	queryset = Child.objects.all()
	serializer_class = ChildSerializer
	model = Child
	permission_classes = [IsAuthenticated, SupervisorPermissions|CaseworkerPermissions|FosterParentPermissions]
	
class FosterFamilyViewSet(RBACMixin, viewsets.ModelViewSet):
	queryset = FosterFamily.objects.all()
	serializer_class = FosterFamilySerializer
	model = FosterFamily
	permission_classes = [IsAuthenticated, SupervisorPermissions|CaseworkerPermissions]

class FosterPlacementViewSet(RBACMixin, viewsets.ModelViewSet):
	queryset = FosterPlacement.objects.all()
	serializer_class = FosterPlacementSerializer
	model = FosterPlacement
	permission_classes = [IsAuthenticated, SupervisorPermissions|CaseworkerPermissions|FosterParentPermissions]

class HealthServiceViewSet(RBACMixin, viewsets.ModelViewSet):
	queryset = HealthService.objects.all()
	serializer_class = HealthServiceSerializer
	model = HealthService
	permission_classes = [IsAuthenticated, SupervisorPermissions|CaseworkerPermissions|FosterParentPermissions]

class ReminderLogViewSet(RBACMixin, viewsets.ModelViewSet):
	queryset = ReminderLog.objects.all()
	serializer_class = ReminderSerializer
	model = ReminderLog
	permission_classes = [IsAuthenticated, SupervisorPermissions|CaseworkerPermissions|FosterParentPermissions]

class ImmunizationRecordViewset(RBACMixin, viewsets.ModelViewSet):
	queryset = ImmunizationRecord
	serializer_class = ImmunizationRecordSerializer
	model = ImmunizationRecord
	permission_classes = [IsAuthenticated, SupervisorPermissions|CaseworkerPermissions|FosterParentPermissions]
