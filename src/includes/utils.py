import json
from typing import TypeVar, Set, Union

from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Model
from rest_framework import serializers

DJANGO_MODEL = TypeVar("DJANGO_MODEL", bound=Model)


def str_to_bool(value: Union[str, bool]) -> bool:
    if type(value) == str:
        truthy_values = ["true", "1", "yes"]
        return value.lower() in truthy_values
    return value


def model_to_dict(
    instance: DJANGO_MODEL,
    exclude_fields: Set[str] = set(),
    **kwargs,
):
    """
    Convert a model instance to dict.
    """

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
