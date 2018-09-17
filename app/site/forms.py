from datetime import date

from django import forms
from django.core.exceptions import ValidationError, ObjectDoesNotExist

from core.models import Book, Author

__all__ = (
    'BaseAuthorFormSet',
    'AuthorForm',
    'BookForm',
    'delete_book',
)


class BaseAuthorFormSet(forms.BaseFormSet):

    def __init__(self, *args, **kwargs):
        self.instances = kwargs.pop('instances', [])
        super(BaseAuthorFormSet, self).__init__(*args, **kwargs)

    def get_form_kwargs(self, index):
        form_kwargs = super(BaseAuthorFormSet, self).get_form_kwargs(index)
        if index < len(self.instances):
            form_kwargs['instance'] = self.instances[index]
        return form_kwargs

    def clean(self):
        if any(self.errors):
            return
        authors_name = []
        for form in self.forms:
            full_name = form.cleaned_data.get('full_name', '')
            if full_name in authors_name:
                raise ValidationError("Authors of the book is duplicated.")
            authors_name.append(full_name)

    def add_authors_to(self, book):
        authors = []

        for form in self.forms:
            author_data = form.cleaned_data
            full_name = author_data.get('full_name', '')
            info = author_data.get('info', '')
            try:
                author = Author.objects.get(full_name=full_name)
                if info:
                    author.info = info
                    author.save()
            except ObjectDoesNotExist:
                author = Author(**author_data)
                author.save()
            authors.append(author)

        book.set_authors(authors)


class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['full_name', 'info']

    def clean(self):
        cleaned_data = self.cleaned_data
        return cleaned_data


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'isbn', 'price', 'publish_date']

    def __init__(self, *args, **kwargs):
        super(BookForm, self).__init__(*args, **kwargs)
        if self.initial:
            self.initial.update({
                'publish_date': self.instance.get_publish_date,
            })

    def clean_publish_date(self):
        publish_date = self.cleaned_data['publish_date']
        if publish_date > date.today():
            raise ValidationError("The book should already be published.")
        return publish_date
