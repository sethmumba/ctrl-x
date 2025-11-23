from django.contrib.auth.models import User
from orders.models import Order

def assign_least_busy_staff():
    """
    Finds staff user with the fewest active tasks.
    Staff must have is_staff=True.
    """
    staff_members = User.objects.filter(is_staff=True)

    if not staff_members.exists():
        return None

    # Choose staff with least active assigned orders
    staff_loads = {
        staff: Order.objects.filter(assigned_staff=staff, progress__in=[
            'paid', 'assigned', 'started', 'products', 'branding', 'review'
        ]).count()
        for staff in staff_members
    }

    # return staff with fewest tasks
    return min(staff_loads, key=staff_loads.get)
