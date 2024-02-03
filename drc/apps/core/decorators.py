from functools import wraps
from django.views.decorators.cache import cache_page
from django.utils.decorators import available_attrs
from django.core.cache import cache

def cache_per_user(timeout):
    def decorator(view_func):
        @wraps(view_func, assigned=available_attrs(view_func))
        def _wrapped_view(request, *args, **kwargs):

            ### cache pages for all users ###
            # user_id = 'unauth'
            # if request.user.is_authenticated:
            #     user_id = request.user.id

            ### cache pages for unauth users only ###
            if request.user.is_authenticated == False:
                return cache_page(timeout, key_prefix="_auth_%s_" % request.user.is_authenticated)(view_func)(request, *args, **kwargs)
            else:
                return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator