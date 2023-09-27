import json
import threading
from functools import reduce
from typing import Set, Type, TypeVar, Union

from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Model
from django.utils.crypto import get_random_string
from rest_framework import serializers

DJANGO_MODEL = TypeVar("DJANGO_MODEL", bound=Model)
GLOBAL_LOCK = threading.Lock()


def str_to_bool(value: Union[str, bool]) -> bool:
    if type(value) == str:
        truthy_values = ["true", "1", "yes"]
        return value.lower() in truthy_values
    return value


def model_to_dict(
    instance: DJANGO_MODEL,
    exclude_fields: Set[str] = None,
    **kwargs,
):
    """
    Convert a model instance to dict.
    """
    if exclude_fields:
        exclude_fields = {field for field in exclude_fields if hasattr(instance, field)}

    class Serializer(serializers.ModelSerializer):
        class Meta:
            model = type(instance) if type(instance) != list else type(instance[0])
            depth = 1
            exclude = tuple(exclude_fields)

    serializer = Serializer(instance)
    parsed_data: dict = json.loads(json.dumps(serializer.data), cls=DjangoJSONEncoder)
    parsed_data.update(kwargs)
    return parsed_data


def generate_sec_id(
    prefix: str,
    model: Type[DJANGO_MODEL],
    sec_id_field: str,
) -> str:
    """
    Creates a date generated id

    Args:
        sec_id_field:
        model:
        prefix: prefix for item code

    Returns:
        str: item code
    """
    serial_no = 1
    last_object = model.objects.last()
    if last_object:
        value = getattr(last_object, sec_id_field)
        last_character = value[-1]
        if str(last_character).isdigit():
            serial_no = int(last_character) + 1
    unique_id = f"{prefix}-{get_random_string(5)}-{serial_no}"
    return unique_id
