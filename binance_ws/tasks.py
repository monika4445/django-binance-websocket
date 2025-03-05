from celery import shared_task
from .models import CryptoPrice
from datetime import timedelta
from django.utils.timezone import now

@shared_task
def cleanup_old_prices():
    """Deletes price records older than 24 hours to save storage."""
    one_day_ago = now() - timedelta(days=1)
    deleted_count, _ = CryptoPrice.objects.filter(timestamp__lt=one_day_ago).delete()
    return f"Deleted {deleted_count} old price records"
