from datetime import datetime
from zoneinfo import ZoneInfo

from django.conf import settings
from django.db.models import Q, Model
from django.http import Http404
from rest_framework import serializers


def create_serializer(fields: dict) -> type(serializers.Serializer):
    field_mapping = {
        int: serializers.IntegerField,
        str: serializers.CharField,
        bool: serializers.BooleanField,
        float: serializers.FloatField,
    }

    serializer_fields = {}
    for field_name, field_type in fields.items():
        serializer_field = field_mapping.get(field_type)
        if not serializer_field:
            raise TypeError(f"Unsupported field type: {field_type}")
        serializer_fields[field_name] = serializer_field()

    return type("DynamicSerializer", (serializers.Serializer,), serializer_fields)


def now(timezone: str = settings.TIME_ZONE):
    return datetime.now(ZoneInfo(timezone))


def get_object(
        model,
        filters: dict = None,
        select_related: list = None,
        prefetch_related: list = None,
        q_objects: Q = None,
        *args,
        **kwargs,
):
    """
    Retrieve a single object from the database with optional filters,
    select_related, and prefetch_related optimizations.

    Args:
        model: Django model class to query.
        filters (dict): Additional keyword filters to apply.
        select_related (list): Related fields for SQL JOIN optimization.
        prefetch_related (list): Related fields for queryset prefetching.
        q_objects: Positional arguments for filtering (e.g., Q objects).
        **kwargs: Additional keyword arguments for filtering.

    Returns:
        obj: The retrieved object, or raises Http404 if not found.
    """
    filters = filters or {}
    select_related = select_related or []
    prefetch_related = prefetch_related or []
    q_objects = q_objects or Q()

    filters.update(**kwargs)

    # Apply filters and relations
    queryset = (
        model.objects
        .prefetch_related(*prefetch_related)
        .select_related(*select_related)
        .filter(q_objects, *args, **filters)  # Merge filters and kwargs
    )

    obj = queryset.first()
    if not obj:
        raise Http404
    return obj
