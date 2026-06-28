from django.contrib import admin
from .models import CustomUser, Asset, InventoryItem, Assignment, RepairTicket


@admin.register(CustomUser)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'role']
    list_filter = ['role']
    search_fields = ['username']


@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    list_display = ['name', 'type', 'serial_number', 'status']
    list_filter = ['status']
    search_fields = ['name', 'serial_number']


@admin.register(InventoryItem)
class InventoryAdmin(admin.ModelAdmin):
    list_display = ['item_type', 'quantity', 'threshold']


@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ['asset', 'employee', 'date_assigned', 'date_returned']


@admin.register(RepairTicket)
class RepairAdmin(admin.ModelAdmin):
    list_display = ['asset', 'status', 'technician']
    list_filter = ['status']
