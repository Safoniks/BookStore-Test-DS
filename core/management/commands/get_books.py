from django.core import serializers
from django.core.management.base import BaseCommand, CommandError

from core.models import Book

ORDER_BY = 'publish_date'
ORDER_CHOICES = {
    'asc': '',
    'desc': '-'
}


def get_ordered_books(order=None):
    books = Book.objects.all()
    if order is None:
        return books
    else:
        order_by = ORDER_CHOICES.get(order, '') + ORDER_BY
        return books.order_by(order_by)


class Command(BaseCommand):
    help = 'Display list of books with possibility to order by publish date field defining ordering	(asc/desc)'

    def add_arguments(self, parser):
        parser.add_argument('-o', '--order', type=str, help='Define a books ordering(asc/desc)', )

    def handle(self, *args, **kwargs):
        order = kwargs['order']
        if order is not None and order not in ORDER_CHOICES:
            raise CommandError('Available variants of the --order argument are %s' % str(tuple(ORDER_CHOICES.keys())))

        books = get_ordered_books(order)
        for idx, book in enumerate(books):
            serialized_obj = serializers.serialize('json', [book, ], use_natural_foreign_keys=True).strip("[]")
            self.stdout.write('{index}. {obj}'.format(index=idx+1, obj=serialized_obj))
