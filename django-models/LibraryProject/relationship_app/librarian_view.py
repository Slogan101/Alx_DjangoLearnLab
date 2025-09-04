from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test
from .utils.role_checker import is_librarian



@user_passes_test(is_librarian)
def librarianview(request):
    return render(request, 'relationship_app/librarian_view.html')