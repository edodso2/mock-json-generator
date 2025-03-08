"""
Utility for generating mock data functions based on text descriptions.

This utility uses a zero-shot classification model to match text descriptions
to appropriate Faker functions for generating synthetic data.
"""

from transformers import pipeline
from faker import Faker

fake = Faker()

# Create a dictionary of Faker functions with descriptive labels
faker_functions = {
    "person name": fake.name,
    "first name": fake.first_name,
    "last name": fake.last_name,
    "email address": fake.email,
    "phone number": fake.phone_number,
    "street address": fake.street_address,
    "city name": fake.city,
    "state name": fake.state,
    "country name": fake.country,
    "zip code": fake.zipcode,
    "job title": fake.job,
    "company name": fake.company,
    "credit card number": fake.credit_card_number,
    "date of birth": fake.date_of_birth,
    "username": fake.user_name,
    "website url": fake.url,
    "paragraph text": fake.paragraph,
    "sentence text": fake.sentence,
}


def get_highest_score_functions(result, faker_functions, threshold=0.18):
    """
    Process model results and map sequences to appropriate Faker functions.

    Args:
        result: The classification results from the model
        faker_functions: Dictionary mapping labels to Faker functions
        threshold: Minimum confidence score to assign a function (default: 0.18)

    Returns:
        dict: Mapping of input sequences to corresponding Faker functions
    """
    sequence_to_function = {}
    for item in result:
        sequence = item["sequence"]
        label = item["labels"][0]
        score = item["scores"][0]
        if score >= threshold:
            sequence_to_function[sequence] = faker_functions.get(label)
        else:
            sequence_to_function[sequence] = None
    return sequence_to_function


def get_functions_for_descriptions(descriptions):
    """
    Get mock data functions based on descriptions or property names.

    Uses zero-shot classification to match text descriptions to appropriate
    Faker functions for generating synthetic data.

    Args:
        descriptions: Array of descriptions or property names to classify

    Returns:
        dict: Mapping of descriptions to corresponding mock data functions
    """
    # Create pipeline with Facebook's BART model for zero-shot classification
    pipe = pipeline(model="facebook/bart-large-mnli")

    # Call pipeline with descriptions and available Faker function labels
    result = pipe(descriptions, candidate_labels=list(faker_functions.keys()))

    # Process results using helper function with default confidence threshold
    return get_highest_score_functions(result, faker_functions, threshold=0.18)
