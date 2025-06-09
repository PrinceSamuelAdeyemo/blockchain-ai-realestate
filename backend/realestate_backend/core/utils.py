from functools import wraps
from django.http import JsonResponse

def web3_session_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not hasattr(request, 'web3_user'):
            return JsonResponse(
                {'error': 'Web3 session required'}, 
                status=401
            )
        return view_func(request, *args, **kwargs)
    return _wrapped_view