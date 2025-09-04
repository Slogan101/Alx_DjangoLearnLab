from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test
from .utils.role_checker import is_admin



@user_passes_test(is_admin)
def adminview(request):
    return render(request, 'relationship_app/admin_view.html')