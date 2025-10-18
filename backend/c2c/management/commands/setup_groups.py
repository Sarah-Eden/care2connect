from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from c2c.models import Child, Case, FosterFamily, FosterPlacement, HealthService, ImmunizationRecord, ReminderLog

class Command(BaseCommand):
	help = 'Create groups for user roles and assign permissions'

	def handle(self, *args, **kwargs):
		# Create groups
		supervisor_group, created = Group.objects.get_or_create(name='Supervisor')
		caseworker_group, created = Group.objects.get_or_create(name='Caseworker')
		fosterparent_group, created = Group.objects.get_or_create(name='FosterParent')

		child_type = ContentType.objects.get_for_model(Child)
		case_type = ContentType.objects.get_for_model(Case)
		family_type = ContentType.objects.get_for_model(FosterFamily)
		placement_type = ContentType.objects.get_for_model(FosterPlacement)
		health_type = ContentType.objects.get_for_model(HealthService)
		reminder_type = ContentType.objects.get_for_model(ReminderLog)
		immuniztion_type = ContentType.objects.get_for_model(ImmunizationRecord)

		# Supervisor permissions: Full CRUD on Child, Case, FosterFamily, FosterPlacement, HealthService, and view on ReminderLog
		supervisor_permissions = [
			# Child model permissions
			Permission.objects.get(codename='add_child', content_type=child_type),
			Permission.objects.get(codename='change_child', content_type=child_type),
			Permission.objects.get(codename='delete_child', content_type=child_type),
			Permission.objects.get(codename='view_child', content_type=child_type),
			# Case model permissions
			Permission.objects.get(codename='add_case', content_type=case_type),
			Permission.objects.get(codename='change_case', content_type=case_type),
			Permission.objects.get(codename='delete_case', content_type=case_type),
			Permission.objects.get(codename='view_case', content_type=case_type),
			# FosterFamily model permissions
			Permission.objects.get(codename='add_fosterfamily', content_type=family_type),
			Permission.objects.get(codename='change_fosterfamily', content_type=family_type),
			Permission.objects.get(codename='delete_fosterfamily', content_type=family_type),
			Permission.objects.get(codename='view_fosterfamily', content_type=family_type),
			# FosterPlacement model permissions
			Permission.objects.get(codename='add_fosterplacement', content_type=placement_type),
			Permission.objects.get(codename='change_fosterplacement', content_type=placement_type),
			Permission.objects.get(codename='delete_fosterplacement', content_type=placement_type),
			Permission.objects.get(codename='view_fosterplacement', content_type=placement_type),
			# HealthService model permissions
			Permission.objects.get(codename='add_healthservice', content_type=health_type),
			Permission.objects.get(codename='change_healthservice', content_type=health_type),
			Permission.objects.get(codename='delete_healthservice', content_type=health_type),
			Permission.objects.get(codename='view_healthservice', content_type=health_type),
			# ImmunizationRecord model permissions
			Permission.objects.get(codename='add_immunizationrecord', content_type=immuniztion_type),
			Permission.objects.get(codename='change_immunizationrecord', content_type=immuniztion_type),
			Permission.objects.get(codename='delete_immunizationrecord', content_type=immuniztion_type),
			Permission.objects.get(codename='view_immunizationrecord', content_type=immuniztion_type),
			# ReminderLog model permissions
			Permission.objects.get(codename='view_reminderlog', content_type=reminder_type)
		]
		supervisor_group.permissions.set(supervisor_permissions)

		# Caseworker permissions: read/limited write on child, create, read, write on Case, HealthService & FosterPlacement, read on FosterFamily & ReminderLog
		caseworker_permissions = [
			# Child model permissions
			Permission.objects.get(codename='change_child', content_type=child_type),
			Permission.objects.get(codename='view_child', content_type=child_type),
			# Case model permissions
			Permission.objects.get(codename='add_case', content_type=case_type),
			Permission.objects.get(codename='change_case', content_type=case_type),
			Permission.objects.get(codename='view_case', content_type=case_type),
			# FosterFamily model permissions
			Permission.objects.get(codename='view_fosterfamily', content_type=family_type),
			# FosterPlacement model permissions
			Permission.objects.get(codename='add_fosterplacement', content_type=placement_type),
			Permission.objects.get(codename='change_fosterplacement', content_type=placement_type),
			Permission.objects.get(codename='view_fosterplacement', content_type=placement_type),
			# HealthService model permissions
			Permission.objects.get(codename='add_healthservice', content_type=health_type),
			Permission.objects.get(codename='change_healthservice', content_type=health_type),
			Permission.objects.get(codename='view_healthservice', content_type=health_type),
			# ImmunizationRecord model permissions
			Permission.objects.get(codename='add_immunizationrecord', content_type=immuniztion_type),
			Permission.objects.get(codename='change_immunizationrecord', content_type=immuniztion_type),
			Permission.objects.get(codename='view_immunizationrecord', content_type=immuniztion_type),
			# ReminderLog model permissions
			Permission.objects.get(codename='view_reminderlog', content_type=reminder_type)
		]
		caseworker_group.permissions.set(caseworker_permissions)

		# Foster Parent permissions: read/limited write on children in their care, read/write on HealthService, read on case & ReminderLog
		fosterparent_permissions = [
			# Child model permissions
			Permission.objects.get(codename='change_child', content_type=child_type),
			Permission.objects.get(codename='view_child', content_type=child_type),
			# Case model permissions
			Permission.objects.get(codename='view_case', content_type=case_type),
			# FosterFamily model permissions
			Permission.objects.get(codename='view_fosterfamily', content_type=family_type),
			# FosterPlacement model permissions
			Permission.objects.get(codename='view_fosterplacement', content_type=placement_type),
			# HealthService model permissions
			Permission.objects.get(codename='change_healthservice', content_type=health_type),
			Permission.objects.get(codename='view_healthservice', content_type=health_type),
			# ImmunizationRecord model permissions
			Permission.objects.get(codename='add_immunizationrecord', content_type=immuniztion_type),
			Permission.objects.get(codename='change_immunizationrecord', content_type=immuniztion_type),
			Permission.objects.get(codename='view_immunizationrecord', content_type=immuniztion_type),
			# ReminderLog model permissions
			Permission.objects.get(codename='view_reminderlog', content_type=reminder_type),		
		]
		fosterparent_group.permissions.set(fosterparent_permissions)

		self.stdout.write(self.style.SUCCESS('Groups and permissions set up successfully!'))
	


