from datetime import date
from decimal import Decimal

from django.contrib.contenttypes.models import ContentType
from django.contrib.admin.models import LogEntry, LogEntryManager
from django.contrib.postgres.fields import JSONField
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, User
from django.utils.encoding import force_text
from django.db import models
from django.core.validators import RegexValidator, MinValueValidator
from django.urls import reverse


__all__ = (
    'Author',
    'Book',
    'WebRequest',
    'AuditLog',
)


class AuthorManager(models.Manager):
    def get_by_natural_key(self, full_name):
        return self.get(full_name=full_name)


class Author(models.Model):
    objects = AuthorManager()

    full_name = models.CharField(max_length=200, unique=True, verbose_name='full name')
    info = models.TextField(null=True, blank=True, verbose_name='information')

    class Meta:
        db_table = 'author'
        verbose_name = 'author'
        verbose_name_plural = 'authors'

    def __str__(self):
        return self.full_name

    def natural_key(self):
        return (
            self.full_name,
        )


class Book(models.Model):
    title = models.CharField(max_length=200, unique=True, verbose_name='title')
    isbn = models.CharField(
        max_length=10,
        unique=True,
        validators=[RegexValidator(
            '^[0-9]{10}$',
            'Length has to be 10 and only digits are allowed.',
            'nomatch'
        )],
        verbose_name='International Standard Book Number'
    )
    price = models.DecimalField(
        max_digits=8, decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'), message='Only positive number are allowed.')],
        verbose_name='price')
    publish_date = models.DateField(null=True, verbose_name='publish date')
    authors = models.ManyToManyField('Author')

    class Meta:
        db_table = 'book'
        verbose_name = 'book'
        verbose_name_plural = 'books'
        ordering = ('title',)

    def __str__(self):
        return self.title

    def get_detail_url(self):
        return reverse('site:book_detail', args=[str(self.id)])

    def get_delete_url(self):
        return reverse('site:delete_book', args=[str(self.id)])

    def get_publish_date(self):
        return date.today() if self.publish_date is None else self.publish_date

    def set_authors(self, new_authors):
        old_authors = self.authors.all()

        for author in old_authors:
            if author not in new_authors:
                self.authors.remove(author)
                if author.book_set.count() == 0:
                    author.delete()

        self.authors.add(*new_authors)


class WebRequest(models.Model):
    request = JSONField(default=dict, verbose_name='request')
    date = models.DateTimeField(auto_now_add=True, verbose_name='request')

    class Meta:
        db_table = 'web_request'
        verbose_name = 'web request'
        verbose_name_plural = 'web requests'
        ordering = ('-date', )


class AuditLogEntryManager(LogEntryManager):
    def just_log(self, obj, action, change_message):
        user = User.objects.first()
        if not user:
            user = User.objects.create_superuser('admin', 'admin@mail', 'admin')
        self.log_action(
            user_id=user.id,
            content_type_id=ContentType.objects.get_for_model(obj).pk,
            object_id=obj.pk,
            object_repr=force_text(obj),
            action_flag=action,
            change_message=change_message
        )


class AuditLog(LogEntry):
    objects = AuditLogEntryManager()

    class Meta:
        proxy = True
