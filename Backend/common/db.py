from django.db import transaction

def select_for_update_skip_locked(qs):
    return qs.select_for_update(skip_locked=True)
