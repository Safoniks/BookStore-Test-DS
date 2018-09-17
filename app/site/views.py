from django.core.exceptions import ObjectDoesNotExist
from django.forms import formset_factory
from django.http import Http404
from django.shortcuts import render, redirect

from core.models import Book
from .forms import BookForm, AuthorForm, BaseAuthorFormSet

__all__ = (
    'home',
    'add_book',
    'book_detail',
    'delete_book',
)


def home(request):
    template_name = 'site/content/home.html'
    context = {
        'books': Book.objects.all()
    }
    return render(request, template_name, context)


def add_book(request):
    template_name = 'site/content/book.html'
    AuthorFormSet = formset_factory(AuthorForm, formset=BaseAuthorFormSet, min_num=1, validate_min=True, extra=0)

    if request.method == 'POST':
        form = BookForm(request.POST)
        formset = AuthorFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            book = form.save()
            formset.add_authors_to(book)
            return redirect('site:home')
    else:
        form = BookForm()
        formset = AuthorFormSet()

    context = {
        'form': form,
        'formset': formset,
    }
    return render(request, template_name, context)


def book_detail(request, pk):
    template_name = 'site/content/book.html'
    try:
        book = Book.objects.get(pk=pk)
    except ObjectDoesNotExist:
        raise Http404
    book_authors = book.authors.all()

    extra_forms = book_authors.count() - 1
    extra_forms = 0 if extra_forms < 0 else extra_forms
    AuthorFormSet = formset_factory(
        AuthorForm, formset=BaseAuthorFormSet,
        min_num=1, validate_min=True, extra=extra_forms
    )
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        formset = AuthorFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            book = form.save()
            formset.add_authors_to(book)
            return redirect('site:home')
    else:
        form = BookForm(instance=book)
        formset = AuthorFormSet(instances=book_authors)

    context = {
        'form': form,
        'formset': formset,
        'book': book,
    }
    return render(request, template_name, context)


def delete_book(request, pk):
    try:
        book = Book.objects.get(pk=pk)
    except ObjectDoesNotExist:
        raise Http404

    book.delete()
    return redirect('site:home')
