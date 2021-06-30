import datetime

import pytz
from sqlalchemy import DateTime
from sqlalchemy.types import TypeDecorator


def tzware_datetime():
    """
    Return a timezone aware datetime.

    :return: Datetime
    """
    return datetime.datetime.now(pytz.utc)


class AwareDateTime(TypeDecorator):
    """
    A DateTime type which can only store tz-aware DateTimes.

    Source:
      https://gist.github.com/inklesspen/90b554c864b99340747e
    """

    cache_ok = True
    impl = DateTime(timezone=True)

    def process_bind_param(self, value, dialect):
        if isinstance(value, datetime.datetime) and value.tzinfo is None:
            raise ValueError("{!r} must be TZ-aware".format(value))
        return value

    def __repr__(self):
        return "AwareDateTime()"
