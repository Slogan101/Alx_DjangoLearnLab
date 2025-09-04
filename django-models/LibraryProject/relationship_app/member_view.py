from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test
from .utils.role_checker import is_member


@user_passes_test(is_member)
def memberview(request):
    return render(request, 'relationship_app/member_view.html')