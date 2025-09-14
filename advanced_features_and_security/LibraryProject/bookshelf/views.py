from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import permission_required
from .models import Book
from .forms import BookForm

# Create your views here.

@permission_required('bookshelf.can_view', raise_exception=True)
def booklist(request):
    book = Book.objects.all()
    return render(request, 'bookshelf/book_list.html', {'books': book})

@permission_required('bookshelf.can_create', raise_exception=True)
def book_create(request):
    if request.method == 'POST':
        form = BookForm(request.Post)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookForm
    return render(request, 'bookshelf/book_form.html', {'form': form})

@permission_required('bookshelf.can_edit', raise_exception=True)
def book_edit(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookForm(instance=book)
    return render(request, 'bookshelf/book_form.html', {'form': form})


@permission_required('bookshelf.can_delete', raise_exception=True)
def book_delete(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        book.delete()
        return redirect('book_list')
    return render(request, 'bookshelf/book_confirm_delete.html', {'book': book})


def search_books(request):
    query = request.GET.get('q', '')
    results = Book.objects.filter(title__icontains=query)
    return render(request, 'bookshelf/search_results.html', {'results': results})


def search_books(request):
    form = BookSearchForm(request.GET)
    results = Book.objects.none()
    if form.is_valid():
        q = form.cleaned_data['q']
        results = Book.objects.filter(title__icontains=q)
    return render(request, 'bookshelf/search_results.html', {'form': form, 'results': results})