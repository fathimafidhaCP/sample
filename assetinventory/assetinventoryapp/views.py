from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout,get_user_model
from django.contrib.auth.decorators import login_required
from .models import Asset, InventoryItem, Assignment, RepairTicket,CustomUser
from django.utils import timezone
from django.shortcuts import get_object_or_404

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            if user.role == 'admin':
                return redirect('admin_dashboard')
            else:
                return redirect('employee_dashboard')

        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})

    return render(request, 'login.html')
        


def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def admin_dashboard(request):
    if request.user.role != 'admin':
        return redirect('employee_dashboard')
    total_assets = Asset.objects.count()
    total_inventory = InventoryItem.objects.count()
    total_assigned = Assignment.objects.count()
    total_repairs = RepairTicket.objects.count()

    context = {
        'total_assets': total_assets,
        'total_inventory': total_inventory,
        'total_assigned': total_assigned,
        'total_repairs': total_repairs,
    }

    return render(request, 'admin_dashboard.html', context)
    

@login_required
def employee_dashboard(request):
    if request.user.role != 'employee':
        return redirect('admin_dashboard')
    my_assets = Assignment.objects.filter(employee=request.user)
    my_repairs = RepairTicket.objects.all()

    context = {
        'my_assets': my_assets,
        'my_repairs': my_repairs,
    }

    return render(request, 'employee_dashboard.html', context)

@login_required
def add_asset(request):
    if request.method == 'POST':
        name = request.POST['name']
        asset_type = request.POST['type']
        serial = request.POST['serial']
        status = request.POST['status']
        purchase_date = request.POST.get('purchase_date')

        Asset.objects.create(
            name=name,
            type=asset_type,
            serial_number=serial,
            status=status,
            purchase_date=purchase_date 
        )

        return redirect('admin_dashboard')

    return render(request, 'add_asset.html')

User = get_user_model()


@login_required
def assign_asset(request):
    if request.user.role != 'admin':
        return redirect('employee_dashboard')

    assets = Asset.objects.all()
    employees = User.objects.filter(role='employee')

    if request.method == 'POST':
        asset_id = request.POST.get('asset')
        employee_id = request.POST.get('employee')

        asset = get_object_or_404(Asset, id=asset_id)
        employee = get_object_or_404(User, id=employee_id)

        Assignment.objects.create(
            asset=asset,
            employee=employee,
            date_assigned=timezone.now().date()   
        )

        # optional but important
        asset.status = 'assigned'
        asset.save()

        return redirect('admin_dashboard')

    return render(request, 'assign_asset.html', {
        'assets': assets,
        'employees': employees
    })

@login_required
def raise_ticket(request):
    my_assets = Assignment.objects.filter(employee=request.user)

    if request.method == 'POST':
        asset_id = request.POST.get('asset')  
        issue = request.POST.get('issue')

        if not asset_id:
            return render(request, 'raise_ticket.html', {
                'error': 'Please select an asset',
                'my_assets': my_assets
            })

        try:
            asset = Asset.objects.get(id=asset_id)
        except Asset.DoesNotExist:
            return render(request, 'raise_ticket.html', {
                'error': 'Invalid asset selected',
                'my_assets': my_assets
            })

        RepairTicket.objects.create(
            asset=asset,
            issue=issue,
            status='pending'
        )

        return redirect('employee_dashboard')

    return render(request, 'raise_ticket.html', {
        'my_assets': my_assets
    })
