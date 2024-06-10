import datetime
from django.utils import timezone


def convert_unix_to_datetime(unix_timestamp):
    # Convert Unix timestamp in milliseconds to seconds
    timestamp_in_seconds = unix_timestamp / 1000

    # Convert Unix timestamp to a naive datetime object
    naive_datetime = datetime.datetime.fromtimestamp(timestamp_in_seconds)

    # Ensure the naive datetime is timezone-aware
    current_datetime = timezone.make_aware(naive_datetime, timezone.get_current_timezone())

    return current_datetime
