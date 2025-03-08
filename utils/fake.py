import random

def generate_mock_data(schema, faker_mapping):
    """
    Generate mock data based on a JSON schema.
    For integer and boolean, use custom logic to generate fake data
    For remaining types, call the corresponding faker function if available.

    Args:
        schema (dict): The JSON schema
        faker_mapping (dict): Mapping of descriptions/property names to faker functions

    Returns:
        dict: Generated mock data
    """
    result = {}

    if "properties" in schema:
        for prop_name, prop_schema in schema["properties"].items():
            if prop_schema.get("type") == "object":
                # Recursively process objects
                result[prop_name] = generate_mock_data(prop_schema, faker_mapping)
            elif prop_schema.get("type") == "integer":
                # Check if min/max properties exist for bounds
                minimum = prop_schema.get("minimum")
                maximum = prop_schema.get("maximum")

                if minimum is not None and maximum is not None:
                    result[prop_name] = random.randint(minimum, maximum)
                elif minimum is not None:
                    result[prop_name] = random.randint(
                        minimum, minimum + 100
                    )  # Arbitrary upper bound
                elif maximum is not None:
                    result[prop_name] = random.randint(
                        0, maximum
                    )  # Assume 0 as lower bound
                else:
                    result[prop_name] = random.randint(0, 100)  # Default range
            elif prop_schema.get("type") == "boolean":
                result[prop_name] = random.choice(
                    [True, False]
                )  # Randomly pick True or False
            else:
                # For non-objects, try to find a faker function
                description = prop_schema.get("description", "")

                # Look for faker function by description or property name
                faker_func = None
                if description in faker_mapping:
                    faker_func = faker_mapping[description]
                elif prop_name in faker_mapping:
                    faker_func = faker_mapping[prop_name]

                # Call faker function if found, otherwise set to None
                result[prop_name] = faker_func() if faker_func else None

    return result


# Example usage:
if __name__ == "__main__":
    from faker import Faker

    fake = Faker()

    sample_schema = {
        "type": "object",
        "properties": {
            "name": {"type": "string", "description": "The person's full name"},
            "age": {"type": "integer"},
            "address": {
                "type": "object",
                "properties": {
                    "street": {
                        "type": "string",
                        "description": "Street name and number",
                    },
                    "city": {"type": "string"},
                },
            },
        },
    }

    # Create faker function mapping
    faker_mapping = {
        "The person's full name": fake.name,
        "age": fake.random_int,
        "Street name and number": fake.street_address,
        "city": fake.city,
    }

    # Generate mock data
    mock_data = generate_mock_data(sample_schema, faker_mapping)
    print(mock_data)
