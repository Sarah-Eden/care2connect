from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from c2c.models import (Child, Case, FosterFamily, FosterPlacement, HealthService, ImmunizationRecord, ReminderLog)

ROLE_DEFINITIONS = {
    'Supervisor': [
        (Child, ['add', 'change', 'delete', 'view']),
        (Case, ['add', 'change', 'delete', 'view']),
        (FosterFamily, ['add', 'change', 'delete', 'view']),
        (FosterPlacement, ['add', 'change', 'delete', 'view']),
        (HealthService, ['add', 'change', 'delete', 'view']),
        (ImmunizationRecord, ['add', 'change', 'delete', 'view']),
        (ReminderLog, ['view']),
	],
    
    'Caseworker': [
        (Child, ['change', 'view']),
        (Case, ['view']),
        (FosterFamily, ['view']),
        (FosterPlacement, ['add', 'change', 'view']),
        (HealthService, ['change', 'view']),
        (ImmunizationRecord, ['view']),
        (ReminderLog, ['view']),
	],
    
	'FosterParent': [
        (Child, ['change', 'view']),
        (Case, ['view']),
        (FosterFamily, ['view']),
        (FosterPlacement, ['view']),
        (HealthService, ['change', 'view']),
        (ImmunizationRecord, ['view']),
        (ReminderLog, ['view']),
	],
}

class Command(BaseCommand):
    help = 'Create role groups and assign model level permissions'
    
    def handle(self, *args, **kwargs):
        for role_name, model_permissions in ROLE_DEFINITIONS.items():
            group, _ = Group.objects.get_or_create(name=role_name)
            permissions = []
            
            for model_class, actions in model_permissions:
                ct = ContentType.objects.get_for_model(model_class)
                model_name = model_class._meta.model_name
                
                for action in actions:
                    permissions.append(Permission.objects.get(codename=f'{action}_{model_name}', content_type=ct))
                    
            group.permissions.set(permissions)
            
        self.stdout.write(self.style.SUCCESS('Groups and permissions set up successfully'))