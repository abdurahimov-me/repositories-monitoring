from dataclasses import dataclass
from datetime import datetime
from typing import Type
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


@dataclass
class CheckoutManager:
    model: Type[Model]
    balance_field: str = 'balance'

    def __add__(self, other):
        return self.add(other)

    def __radd__(self, other):
        return self.add(other)

    def __sub__(self, other):
        return self.add(-other)

    def __rsub__(self, other):
        raise NotImplementedError("Subtraction with reversed operands is not supported.")

    @property
    def __checkout(self):
        # Get the first object, or return None if no objects exist
        return self.model.objects.first()

    @property
    def balance(self):
        checkout = self.__checkout
        if checkout:
            return getattr(checkout, self.balance_field)
        raise ValueError("No checkout instance found.")

    def add(self, amount):
        checkout = self.__checkout
        if checkout:
            current_balance = getattr(checkout, self.balance_field)
            new_balance = current_balance + amount
            setattr(checkout, self.balance_field, new_balance)
            checkout.save()
            return new_balance
        else:
            raise ValueError("No checkout instance found. Cannot add balance.")
