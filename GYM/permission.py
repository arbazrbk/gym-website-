from functools import wraps
from django.shortcuts import redirect, render
from django.contrib import messages
from .models import SubcriptionModel


# ============================================================
# PLAN HIERARCHY: Free (no sub) < Silver < Pro
# ============================================================
PLAN_LEVELS = {
    'free': 0,
    'basic': 0,
    'silver': 1,
    'premium': 1,
    'pro': 2,
}


def get_user_plan_level(user):
    """Get the user's current plan level (0=free, 1=silver, 2=pro)"""
    if not user.is_authenticated:
        return -1  # not logged in
    
    sub = SubcriptionModel.objects.filter(user_id=user, status='active').first()
    if not sub:
        return 0  # free / no subscription
    
    plan_name = sub.subcription_plan.lower().strip()
    return PLAN_LEVELS.get(plan_name, 0)


def get_user_plan_name(user):
    """Get the user's current plan name"""
    if not user.is_authenticated:
        return 'Guest'
    
    sub = SubcriptionModel.objects.filter(user_id=user, status='active').first()
    if not sub:
        return 'Free'
    
    return sub.subcription_plan.capitalize()


# ============================================================
# DECORATORS
# ============================================================

def login_required_custom(view_func):
    """User must be logged in"""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'Please login first.')
            return redirect('loginview')
        return view_func(request, *args, **kwargs)
    return wrapper


def subscription_required(min_plan='silver'):
    """
    User must have at least the specified plan.
    Admin (is_superuser / is_staff) always has full access.
    Usage: @subscription_required('silver') or @subscription_required('pro')
    """
    min_level = PLAN_LEVELS.get(min_plan.lower(), 1)
    
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            # Check login first
            if not request.user.is_authenticated:
                messages.error(request, 'Please login first.')
                return redirect('loginview')
            
            # Admin/Staff bypass - full access
            if request.user.is_superuser or request.user.is_staff:
                return view_func(request, *args, **kwargs)
            
            user_level = get_user_plan_level(request.user)
            user_plan = get_user_plan_name(request.user)
            
            if user_level < min_level:
                # Plan names for display
                plan_names = {0: 'Free', 1: 'Silver', 2: 'Pro'}
                required_plan = plan_names.get(min_level, min_plan.capitalize())
                
                context = {
                    'required_plan': required_plan,
                    'user_plan': user_plan,
                    'user_level': user_level,
                    'min_level': min_level,
                }
                return render(request, 'GYM/access_denied.html', context)
            
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator


def silver_required(view_func):
    """Shortcut: requires Silver plan or above"""
    return subscription_required('silver')(view_func)


def pro_required(view_func):
    """Shortcut: requires Pro plan"""
    return subscription_required('pro')(view_func)
