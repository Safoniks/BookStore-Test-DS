from django.db.models.signals import pre_delete, post_delete, post_save
from django.dispatch import receiver
from django.contrib.admin.models import ADDITION, CHANGE, DELETION

from core.models import Book, AuditLog


@receiver(pre_delete, sender=Book)
def pre_delete_book(sender, instance, **kwargs):
    for author in instance.authors.all():
        if author.book_set.count() == 1 and instance in author.book_set.all():
            author.delete()


@receiver(post_save, sender=Book)
def post_save_handler(sender, instance, created, **kwargs):
    if created:
        AuditLog.objects.just_log(instance, ADDITION, 'Added')
    else:
        AuditLog.objects.just_log(instance, CHANGE, 'Changed')


@receiver(post_delete, sender=Book)
def post_delete_handler(sender, instance, **kwargs):
    AuditLog.objects.just_log(instance, DELETION, 'Deleted')
