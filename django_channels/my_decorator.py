from django.shortcuts import redirect


def login_required(view_func):
    def wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')  # Redirect to login page if user is not authenticated
        return view_func(request, *args, **kwargs)

    return wrapped_view
