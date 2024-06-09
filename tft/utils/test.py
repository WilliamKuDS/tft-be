import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tft_django.settings")
django.setup()

from datetime import datetime
from tft.service.patch_service import getPatchFromDate
from tft.utils.convert_unix_to_datetime import convert_unix_to_datetime

#current_datetime = datetime(2024, 6, 9, 12, 0, 0)
current_datetime = convert_unix_to_datetime(1717718577000)
print(getPatchFromDate(current_datetime))
