from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from .models import Change


@receiver(post_save, dispatch_uid='update_signal')
@receiver(pre_delete, dispatch_uid='delete_signal')
def change_handler(sender, instance, created=None, **kwargs):
    st = ''
    if sender is not Change:
        try:
            if created is None:
                st = 'D'
            elif created:
                st = 'C'
            else:
                st = 'U'
            c = Change(
                status=st,
                object=instance.pk,
                model=sender.__name__,
            )
            c.save()
        except:
            pass
