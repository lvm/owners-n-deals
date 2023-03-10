import datetime
from typing import Any


def simple_serializer(dct: dict) -> dict:
    def sanitize(value: Any) -> str:
        if isinstance(value, datetime.datetime):
            return value.isoformat()
        if isinstance(value, dict):
            return {k: sanitize(v) for k, v in value.items()}
        if isinstance(value, list):
            return [sanitize(v) for v in value]
        else:
            return value

    return {key: sanitize(value) for key, value in dct.items()}


def create_or_update(Model, pk, data):
    obj = None
    try:
        obj = Model.objects.get(pk=pk)
        for key, value in data.items():
            setattr(obj, key, value)
        obj.save()
    except Model.DoesNotExist:
        obj = Model(**data)
        obj.save()

    return obj
