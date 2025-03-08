import json
import datetime
from decimal import Decimal
from uuid import UUID


class CustomJSONEncoder(json.JSONEncoder):
    """
    Custom JSON encoder that handles various Python types that aren't JSON serializable by default:
    - datetime.datetime, datetime.date, datetime.time
    - Decimal
    - UUID
    - Sets
    - Any object with a to_json method
    - Custom objects with __dict__ attribute
    """

    def default(self, obj):
        # Handle datetime objects
        if isinstance(obj, (datetime.datetime, datetime.date)):
            return obj.isoformat()

        # Handle time objects
        if isinstance(obj, datetime.time):
            return obj.isoformat()

        # Handle Decimal objects
        if isinstance(obj, Decimal):
            return float(obj)

        # Handle UUID objects
        if isinstance(obj, UUID):
            return str(obj)

        # Handle set objects
        if isinstance(obj, set):
            return list(obj)

        # Handle objects that have implemented a to_json method
        if hasattr(obj, "to_json"):
            return obj.to_json()

        # Try to convert the object to a dict
        try:
            return obj.__dict__
        except AttributeError:
            pass

        # Let the base class handle it or raise TypeError
        return super().default(obj)


def serialize_to_json(data, pretty=False):
    """
    Serialize Python data to JSON string, handling various Python types.

    Args:
        data: The Python object to serialize
        pretty (bool): Whether to format the JSON with indentation for readability

    Returns:
        str: JSON string representation of the data
    """
    indent = 2 if pretty else None
    return json.dumps(data, cls=CustomJSONEncoder, indent=indent)
