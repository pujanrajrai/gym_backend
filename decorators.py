from django.http import JsonResponse
from django.contrib import auth
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.shortcuts import redirect
from accounts.models import User
from django.http import JsonResponse
from django.shortcuts import render


def has_roles(allowed_roles):
    def decorator(view_function):
        def wrap(request, *args, **kwargs):
            try:
                user = request.user
                if user.is_authenticated:
                    username = request.user
                    if not user.is_blocked:
                        if user.role in allowed_roles:
                            return view_function(request, *args, **kwargs)
                        else:
                            raise PermissionDenied
                    else:
                        auth.logout(request)
                        return HttpResponse('Your account is blocked. Please contact admin')
                else:
                    return redirect('accounts:pages:users:')
            except PermissionDenied:
                return render(request, '403.html', status=403)
            except Exception as e:
                print(e)
                return HttpResponse(f'error occored {e}')
        return wrap
    return decorator
