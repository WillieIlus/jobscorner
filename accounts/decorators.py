from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import redirect


def normal_user_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='accounts:login'):
    '''
    Decorator for views that checks that the logged in user is a normal user,
    redirects to the log-in page if necessary.
    '''
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_normal_user,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


def employer_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='accounts:login'):
    '''
    Decorator for views that checks that the logged in user is a teacher,
    redirects to the log-in page if necessary.
    '''
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_employer,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


class UserRequiredMixin(object):
    """ Making sure that only own user can update """

    def dispatch(self, request, *args, **kwargs):
        response = redirect('accounts:login')
        obj = self.get_object()
        if obj.user != self.request.user:
            return response
        return super(UserRequiredMixin, self).dispatch(request, *args, **kwargs)
