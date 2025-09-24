from rest_framework import serializers
from django.contrib.auth.models import User, Group
from .models import Case, Child, FosterFamily, FosterPlacement, HealthService, ReminderLog
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

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
	
class CaseSerializer(serializers.ModelSerializer):
	class Meta:
		model=Case
		fields = '__all__'
	
class ChildSerializer(serializers.ModelSerializer): 
	class Meta:
		model=Child
		fields = '__all__'

class FosterFamilySerializer(serializers.ModelSerializer):
	class Meta:
		model=FosterFamily
		fields = '__all__'

class FosterPlacementSerializer(serializers.ModelSerializer):
	class Meta:
		model=FosterPlacement
		fields = '__all__'

class HealthServiceSerializer(serializers.ModelSerializer):
	class Meta:
		model=HealthService
		fields = '__all__'

class ReminderSerializer(serializers.ModelSerializer):
	class Meta:
		model=ReminderLog
		fields='__all__'
