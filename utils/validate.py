import json
from jsonschema import validate, exceptions

meta_schema = {
    "type": "object",
    "required": ["type", "properties"],
    "properties": {"type": {"type": "string"}, "properties": {"type": "object"}},
}


def validate_schema_structure(schema_str):
    """
    Parse and Validate a JSON Schema object

    Args:
        schema_str: A valid JSON schema object seralized to a string

        Returns:
        tuple: (bool, object) where:
            - First element is a boolean indicating success (True) or failure (False)
            - Second element is either the validated schema object (on success)
              or an error message string (on failure)
    """

    try:
        schema = json.loads(schema_str)
        validate(instance=schema, schema=meta_schema)
        return True, schema
    except exceptions.ValidationError as e:
        return False, f"Schema structure validation error: {e}"
    except json.JSONDecodeError as e:
        return False, f"Invalid JSON syntax: {str(e)}"
    except Exception as e:
        return False, f"Unexpected error: {str(e)}"
