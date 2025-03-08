def extract_descriptions(schema, path=""):
    """
    Recursively extract all descriptions from a JSON schema.
    If a property doesn't have a description, use its property name.

    Args:
        schema (dict): The JSON schema to extract descriptions from
        path (str): Current path in the schema (for nested properties)

    Returns:
        list: All descriptions found in the schema
    """
    descriptions = []

    # Handle schema description or use path as fallback
    # Skip if type is object
    if schema.get("type") != "object":
        if "description" in schema:
            descriptions.append(schema["description"])
        elif path:  # Only add path if it's not empty (root element)
            descriptions.append(path.split(".")[-1])  # Use the last part of the path

    # Handle properties
    if "properties" in schema:
        for prop_name, prop_schema in schema["properties"].items():
            prop_path = f"{path}.{prop_name}" if path else prop_name
            descriptions.extend(extract_descriptions(prop_schema, prop_path))

    # Handle array items
    if "items" in schema and isinstance(schema["items"], dict):
        item_path = f"{path}[]" if path else "items"
        descriptions.extend(extract_descriptions(schema["items"], item_path))

    # Handle oneOf, anyOf, allOf
    for key in ["oneOf", "anyOf", "allOf"]:
        if key in schema and isinstance(schema[key], list):
            for i, sub_schema in enumerate(schema[key]):
                sub_path = f"{path}.{key}[{i}]" if path else f"{key}[{i}]"
                descriptions.extend(extract_descriptions(sub_schema, sub_path))

    # Handle additional properties
    if "additionalProperties" in schema and isinstance(
        schema["additionalProperties"], dict
    ):
        add_path = f"{path}.additionalProperties" if path else "additionalProperties"
        descriptions.extend(
            extract_descriptions(schema["additionalProperties"], add_path)
        )

    return descriptions


# Example usage:
if __name__ == "__main__":
    sample_schema = {
        "type": "object",
        "description": "A person object",
        "properties": {
            "name": {"type": "string", "description": "The person's full name"},
            "age": {
                "type": "integer",
                # No description for age, will use property name
            },
            "address": {
                "type": "object",
                "description": "The person's address",
                "properties": {
                    "street": {
                        "type": "string",
                        "description": "Street name and number",
                    },
                    "city": {
                        "type": "string"
                        # No description for city, will use property name
                    },
                },
            },
            "hobbies": {
                "type": "array",
                "description": "List of hobbies",
                "items": {"type": "string", "description": "A hobby name"},
            },
        },
    }

    descriptions = extract_descriptions(sample_schema)
    print("Extracted descriptions:")
    for desc in descriptions:
        print(f"- {desc}")
