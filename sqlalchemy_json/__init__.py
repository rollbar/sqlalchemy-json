from sqlalchemy.ext.mutable import (
    Mutable,
    MutableDict)
from sqlalchemy_utils.types.json import JSONType

from . track import (
    TrackedDict,
    TrackedList)

__all__ = 'MutableJson', 'NestedMutableJson'


class _PickleMixin(object):
    def __getstate__(self):
        d = self.__dict__.copy()
        d.pop("_parents", None)
        return d


class NestedMutableDict(TrackedDict, Mutable, _PickleMixin):
    @classmethod
    def coerce(cls, key, value):
        if isinstance(value, cls):
            return value
        if isinstance(value, dict):
            return cls(value)
        return super(cls).coerce(key, value)


class NestedMutableList(TrackedList, Mutable, _PickleMixin):
    @classmethod
    def coerce(cls, key, value):
        if isinstance(value, cls):
            return value
        if isinstance(value, list):
            return cls(value)
        return super(cls).coerce(key, value)


class NestedMutable(Mutable):
    """SQLAlchemy `mutable` extension with nested change tracking."""
    @classmethod
    def coerce(cls, key, value):
        """Convert plain dictionary to NestedMutable."""
        if value is None:
            return value
        if isinstance(value, cls):
            return value
        if isinstance(value, dict):
            return NestedMutableDict.coerce(key, value)
        if isinstance(value, list):
            return NestedMutableList.coerce(key, value)
        return super(cls).coerce(key, value)


class MutableJson(JSONType):
    """JSON type for SQLAlchemy with change tracking at top level."""


class NestedMutableJson(JSONType):
    """JSON type for SQLAlchemy with nested change tracking."""


MutableDict.associate_with(MutableJson)
NestedMutable.associate_with(NestedMutableJson)
