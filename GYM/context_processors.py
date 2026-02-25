from .models import SubcriptionModel
from .permission import get_user_plan_level, get_user_plan_name, PLAN_LEVELS


def subscription_context(request):
    """Add subscription info to all templates"""
    if request.user.is_authenticated:
        active_sub = SubcriptionModel.objects.filter(
            user_id=request.user, 
            status='active'
        ).first()
        
        plan_level = get_user_plan_level(request.user)
        plan_name = get_user_plan_name(request.user)
        
        return {
            'has_active_subscription': active_sub is not None,
            'user_subscription': active_sub,
            'user_plan_level': plan_level,       # 0=free, 1=silver, 2=pro
            'user_plan_name': plan_name,          # "Free", "Silver", "Pro"
            'is_silver_or_above': plan_level >= 1,
            'is_pro': plan_level >= 2,
        }
    return {
        'has_active_subscription': False,
        'user_subscription': None,
        'user_plan_level': -1,
        'user_plan_name': 'Guest',
        'is_silver_or_above': False,
        'is_pro': False,
    }
