from rest_framework import serializers
from django.contrib.auth.models import User, Group
from .models import Case, Child, FosterFamily, FosterPlacement, HealthService, ReminderLog, ImmunizationRecord
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .constants import IMMUNIZATION_DOSES

class UserSerializer(serializers.ModelSerializer):
	groups = serializers.PrimaryKeyRelatedField(queryset=Group.objects.all(), many=True, required=True)

	class Meta:
		model = User
		fields = ['id', 'username', 'password', 'email', 'first_name', 'last_name', 'groups', 'is_active']
		extra_kwargs = {'password': {'write_only': True}}

		def create(self, validated_data):
			groups = validated_data.pop('groups')
			user = User.objects.create_user(**validated_data)
			user.groups.set(groups)
			return user

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
	def validate(self, attrs):
		data = super().validate(attrs)
		user = self.user
		data['groups'] = [group.name for group in user.groups.all()]
		return data

class ChildSerializer(serializers.ModelSerializer): 
	class Meta:
		model=Child
		fields = '__all__'

class CaseSerializer(serializers.ModelSerializer):
	child = ChildSerializer(read_only=True)
	
	class Meta:
		model=Case
		fields = '__all__'
	
	def create(self, validated_data):
		child_id = self.initial_data.get('child')

		if not child_id:
			raise serializers.ValidationError({'child': 'Invalid child ID.'})
		
		try:
			child = Child.objects.get(id=child_id)
		except Child.DoesNotExist:
			raise serializers.ValidationError({'child': 'Invalid child ID.'})
		# Use custom CaseManager for creation
		return Case.objects.create_case(child=child, **validated_data)

	def update(self, instance, validated_data):
		for attr, value in validated_data.items():
			setattr(instance, attr, value)
		instance.save()
		return instance	
	
class FosterFamilySerializer(serializers.ModelSerializer):
	class Meta:
		model=FosterFamily
		fields = '__all__'

class FosterPlacementSerializer(serializers.ModelSerializer):
	class Meta:
		model=FosterPlacement
		fields = '__all__'

class HealthServiceSerializer(serializers.ModelSerializer):
	child=ChildSerializer(read_only=True)
	class Meta:
		model=HealthService
		fields = '__all__'

class ReminderSerializer(serializers.ModelSerializer):
	class Meta:
		model=ReminderLog
		fields='__all__'

class ImmunizationRecordSerializer(serializers.ModelSerializer):
	class Meta:
		model=ImmunizationRecord
		fields='__all__'
	
	def create(self, validated_data):
		validated_data['required_doses'] = IMMUNIZATION_DOSES.get(validated_data['vaccine_name'], 0)
		return super().create(validated_data)
	
	def validate(self, data):
		if data['dose_number'] > data['required_doses']:
			raise serializers.ValidationError('Dose number cannot exceed required doses.')
		
