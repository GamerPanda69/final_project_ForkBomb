# authentication/signals.py
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from banking.models import Account # Import Account from banking app

@receiver(post_save, sender=User)
def create_user_account(sender, instance, created, **kwargs):
    """
    Automatically create an Account when a new User is created.
    """
    if created:
        Account.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_account(sender, instance, **kwargs):
    """
    Ensure the associated Account is saved when the User is saved.
    (Usually handled by cascading saves, but good practice)
    """
    try:
        instance.account.save()
    except Account.DoesNotExist:
        # If account doesn't exist (e.g., for users created before signal), create it
        Account.objects.create(user=instance)