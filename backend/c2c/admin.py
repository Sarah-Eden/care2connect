from django.contrib import admin
from .models import Case, Child, FosterFamily, FosterPlacement, HealthService, ReminderLog

# Inline to display Case within Child
class CaseInline(admin.TabularInline):
	model=Case

# Inline for HealthService within Child
class HealthServiceInline(admin.TabularInline):
	model=HealthService

# Inline to display ReminderLog within HealthService
class ReminderLogInline(admin.TabularInline):
	model=ReminderLog

@admin.register(Child)
class ChildAdmin(admin.ModelAdmin):
	inlines = [CaseInline, HealthServiceInline]
	list_display = ('last_name', 'first_name', 'dob', 'medications', 'allergies')

@admin.register(Case)
class CaseAdmin(admin.ModelAdmin):
	list_display = ('child', 'caseworker', 'status', 'start_date', 'end_date')

@admin.register(FosterFamily)
class FosterFamilyAdmin(admin.ModelAdmin):
	list_display = ('family_name', 'parent1', 'parent2', 'max_occupancy', 'current_occupancy')

@admin.register(FosterPlacement)
class FosterPlacementAdmin(admin.ModelAdmin):
	list_display = ('child', 'foster_family', 'start_date', 'end_date', 'end_reason')

@admin.register(HealthService)
class HealthServiceAdmin(admin.ModelAdmin):
	inlines = [ReminderLogInline]
	list_display = ('child', 'service', 'immunizations', 'due_date', 'completed_date', 'status', 'created_date', 'updated_date')

@admin.register(ReminderLog)
class ReminderLogAdmin(admin.ModelAdmin):
	list_display = ('user', 'service', 'sent_date', 'status')