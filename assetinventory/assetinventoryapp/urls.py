from django.urls import path
from assetinventoryapp import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('employee-dashboard/', views.employee_dashboard, name='employee_dashboard'),
    path('add-asset/', views.add_asset, name='add_asset'),
    path('assign-asset/', views.assign_asset, name='assign_asset'),
    path('raise-ticket/', views.raise_ticket, name='raise_ticket'),
]