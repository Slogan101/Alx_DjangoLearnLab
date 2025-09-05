from django.shortcuts import render, redirect
from relationship_app.models import Book
from .models import Library
from django.views.generic.detail import DetailView
from django.views.generic import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import login
from django.contrib import messages
from django.urls import reverse_lazy
from .utils.role_checker import is_admin, is_member, is_librarian
# Create your views here.





def books(request):
    books = Book.objects.all()
    return render(request, 'relationship_app/list_books.html', {'books': books})

class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'

def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'relationship_app/register.html', {'form': form})

def profile(request):
    return render(request, 'relationship_app/profile.html')




@user_passes_test(is_admin)
def adminview(request):
    return render(request, 'relationship_app/admin_view.html')

@user_passes_test(is_librarian)
def librarianview(request):
    return render(request, 'relationship_app/librarian_view.html')

@user_passes_test(is_member)
def memberview(request):
    return render(request, 'relationship_app/member_view.html')
# class register(CreateView):
#     form_class = UserCreationForm
#     success_url = reverse_lazy('login')
#     template_name = 'relationship_app/register.html'
