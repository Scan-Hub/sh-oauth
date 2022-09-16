# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
import traceback
from datetime import datetime, timezone

from marshmallow import fields, Schema, EXCLUDE


class DatetimeField(fields.Field):
    def _serialize(self, value, attr, obj, **kwargs):
        MIN_YEAR = 1
        MAX_YEAR = 9999
        if isinstance(value, (float, int)):
            if MIN_YEAR * 365 * 86400 <= float(value) <= MAX_YEAR * 365 * 86400:
                return datetime.fromtimestamp(value, tz=timezone.utc)
        return datetime.fromtimestamp(0, tz=timezone.utc)
    default_error_messages =  {
        "required": "Missing data for required field.",
        "null": "Field may not be null.",
        "validator_failed": "Not a valid seconds timestamp.",
    }

    def _deserialize(
            self,
            value,
            *args,
            **kwargs
    ):
        if isinstance(value, datetime):
            return value.replace(tzinfo=timezone.utc).timestamp()

        return value

    def _validate(self, value):
        """Format the value or raise a :exc:`ValidationError` if an error occurs."""
        print('_validate', value)
        if value is None:
            return 0
        if not isinstance(value, (float, int)):
            raise self.make_error("validator_failed", input=value)
        try:
            datetime.fromtimestamp(value, tz=timezone.utc)
        except:
            traceback.print_exc()
            raise self.make_error("validator_failed", input=value)
        return value


class Test(Schema):
    class Meta:
        unknown = EXCLUDE

    day = DatetimeField(required=True)


obj = {
    'day': datetime.utcnow()
}
print(Test().load(obj))
