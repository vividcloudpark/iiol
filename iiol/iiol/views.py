from django.shortcuts import redirect


def site_prefix_redirect(request, path):
    new_path = path.lstrip('/')
    return redirect(new_path)
