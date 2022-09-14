import pydantic
from thaibow.model import Model

def api_external_validator(payload, path):
    try:
        validated_payload = Model(**payload)
        return validated_payload
    except pydantic.ValidationError as ve:
        print(path)
        raise Exception(ve)

