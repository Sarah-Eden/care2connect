from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Case, Child, FosterFamily, FosterPlacement, HealthService, ReminderLog

class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ['id', 'username','email', 'first_name', 'last_name', 'groups', 'is_active']
		read_only_fields = ['id', 'username']

class CaseSerializer(serializers.ModelSerializer):
	class Meta:
		model=Case
		fields = '__all__'
		read_only_fields = ['id', 'child']

class ChildSerializer(serializers.ModelSerializer): 
	class Meta:
		model=Child
		fields = '__all__'
		read_only_fields = ['id', 'dob']

class FosterFamilySerializer(serializers.ModelSerializer):
	class Meta:
		model=FosterFamily
		fields = '__all__'
		read_only_fields = ['id']

class FosterPlacementSerializer(serializers.ModelSerializer):
	class Meta:
		model=FosterPlacement
		fields = '__all__'
		read_only_fields = ['id']

class HealthServiceSerializer(serializers.ModelSerializer):
	class Meta:
		model=HealthService
		fields = '__all__'
		read_only_fields = ['id']

class ReminderSerializer(serializers.ModelSerializer):
	class Meta:
		model=ReminderLog
		fields='__all__'
