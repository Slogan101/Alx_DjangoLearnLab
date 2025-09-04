from django.shortcuts import render
from relationship_app.models import Book, Library
from django.views.generic import ListView, DetailView

# Create your views here.





def books(request):
    books = Book.objects.all()
    return render(request, 'list_books.html', {'books': books})

class LibraryDetailView(DetailView):
    model = Library
    template_name = 'library_detail.html'
    context_object_name = 'library'
