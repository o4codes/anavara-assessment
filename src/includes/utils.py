import json
import re
import threading
from functools import reduce
from typing import TypeVar, Set, Union, Type

from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Model
from django.utils import timezone
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
    CURRENT_YEAR = str(timezone.now().year)
    CURRENT_MONTH = str(timezone.now().month).zfill(2)
    pattern_string = f"{CURRENT_YEAR}{CURRENT_MONTH}"
    re_pattern = re.compile(f"{pattern_string}(.*)")
    serial_no = 1

    with GLOBAL_LOCK:
        filter_kwargs = {
            f"{sec_id_field}__contains": f"{CURRENT_YEAR}{CURRENT_MONTH}",
        }
        objects = model.objects.filter(**filter_kwargs)
        if objects.count() > 0:
            last_object = reduce(
                lambda obj1, obj2: obj1 if obj1.id > obj2.id else obj2, objects
            )
            search_value = getattr(last_object, sec_id_field)
            last_value = re_pattern.findall(search_value)[-1]
            print(last_value)
            if str(last_value).isdigit():
                serial_no = int(re_pattern.findall(search_value)[-1]) + 1
    unique_id = f"{prefix}{CURRENT_YEAR}{CURRENT_MONTH}{serial_no}"
    return unique_id
