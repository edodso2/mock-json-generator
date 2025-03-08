import json
import gradio as gr
from utils.classify import get_functions_for_descriptions
from utils.extract import extract_descriptions
from utils.fake import generate_mock_data
from utils.validate import validate_schema_structure
from utils.serialize_json import serialize_to_json

# Store globally so we don't have to recalculate if
# the schema has not changed
function_mappings = {}


def process_schema(schema):
    """Process the schema and return either mock data or an error message"""
    global function_mappings

    is_valid, result = validate_schema_structure(schema)

    if not is_valid:
        return (
            None,
            result,  # If invalid this will contain the error message
        )

    if not function_mappings:
        descriptions = extract_descriptions(result)
        function_mappings = get_functions_for_descriptions(descriptions)

    mock_data = generate_mock_data(result, function_mappings)

    mock_json = serialize_to_json(mock_data, pretty=True)

    return mock_json, None


def clear_function_mappings():
    global function_mappings
    function_mappings = {}


# Create a default schema example
default_schema = json.dumps(
    {
        "type": "object",
        "description": "A person object",
        "properties": {
            "first_name": {"type": "string", "description": "The person's first name"},
            "last_name": {"type": "string", "description": "The person's last name"},
            "age": {"type": "integer", "minimum": 18, "maximum": 100},
            "email": {"type": "string"},
            "is_active": {"type": "boolean"},
            "address": {
                "type": "object",
                "properties": {
                    "street": {"type": "string"},
                    "city": {"type": "string"},
                    "zip": {"type": "string"},
                },
            },
        },
        "required": ["first_name", "last_name", "age"],
    },
    indent=2,
)

# Create the Gradio interface
with gr.Blocks(theme=gr.themes.Base()) as app:
    gr.Markdown("# JSON Schema Mock Data Generator")
    gr.Markdown(
        "Enter a valid JSON schema and generate mock data that conforms to the schema."
    )

    with gr.Row():
        with gr.Column():
            schema_input = gr.Textbox(
                label="JSON Schema",
                value=default_schema,
                lines=15,
                placeholder="Enter your JSON schema here...",
            )

            generate_btn = gr.Button("Generate Mock Data", variant="primary")

        with gr.Column():
            mock_output = gr.Textbox(
                label="Generated Mock JSON", lines=15, interactive=False
            )

            error_output = gr.Textbox(label="Errors", visible=False, interactive=False)

    def update_output(schema_str):
        mock_data, error = process_schema(schema_str)

        if error:
            return {
                mock_output: None,
                error_output: error,
                error_output: gr.update(visible=True),
            }
        else:
            return {
                mock_output: mock_data,
                error_output: None,
                error_output: gr.update(visible=False),
            }

    schema_input.change(fn=clear_function_mappings, inputs=[], outputs=[])

    generate_btn.click(
        fn=update_output,
        inputs=[schema_input],
        outputs=[mock_output, error_output, error_output],
    )

    gr.Markdown(
        """
    ## Notes
    - Zero Shot Classification will run the first time a mock is generated for a schema. Subsequent generations will be instant.
    - The schema must be valid JSON and comply with JSON Schema Draft 7
    - Required keywords: `type` and `properties` (for object types)
    - Currently Supported types: string, integer, boolean, array, and object
    """
    )

if __name__ == "__main__":
    app.launch()
