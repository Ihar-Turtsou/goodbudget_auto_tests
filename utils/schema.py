import base64
import json
import os

from jsonschema import ValidationError, validate

SCHEMAS_DIR = os.path.join(
    os.path.dirname(os.path.dirname(__file__)), "resources", "schemas"
)


def validate_schema(data: dict, schema_file: str):
    path = os.path.join(SCHEMAS_DIR, schema_file)
    with open(path, "r", encoding="utf-8") as file:
        schema = json.load(file)
    try:
        validate(instance=data, schema=schema)
    except ValidationError as error:
        raise AssertionError(
            f"Schema validation failed for {schema_file}: {error.message}"
        ) from error


def validate_transaction_save_request(form_dict: dict):
    validate_schema(form_dict, "transaction_save_request_form.json")

    decoded = json.loads(base64.b64decode(form_dict["d"]).decode("utf-8"))
    validate_schema(decoded, "transaction_save_request_d.json")
