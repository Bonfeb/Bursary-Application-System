from django.http import HttpResponse
from django.shortcuts import redirect

def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('index')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func

def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):

            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
            if group in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse('You are not authorised to view this page!', status=403)
        return wrapper_func
    return decorator

def admin_only(view_func):
    def wrapper_function(request, *args, **kwargs):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name
        if group == 'applicant':
            return redirect('applicant_dashboard')
        elif group == 'admin':
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponse("You don't have permission to access this page.", status=403)
    return wrapper_function

    def test_decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            return HttpResponse('Test decorator works!')
        return wrapper_func