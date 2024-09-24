import os
import yaml
from yaml.error import YAMLError
from jsonschema import validate, ValidationError

def load_schema():
    try:
        with open("dataset-spec.yaml", 'r') as file:
            return yaml.safe_load(file)
    except FileNotFoundError:
        print("Error: dataset-spec.yaml not found. Please ensure it exists in the root directory.")
        exit(1)
    except YAMLError as e:
        print(f"Error parsing dataset-spec.yaml: {e}")
        exit(1)

schema = load_schema()

def validate_yaml_file(file_path):
    try:
        with open(file_path, 'r') as file:
            data = yaml.safe_load(file)
        validate(instance=data, schema=schema)
        print(f"✅ {file_path} is valid")
        return True
    except YAMLError as e:
        print(f"❌ {file_path} is not valid YAML: {e}")
    except ValidationError as e:
        print(f"❌ {file_path} does not match the schema: {e}")
    return False

def validate_all_yaml_files():
    valid_files = 0
    total_files = 0
    for root, dirs, files in os.walk("datasets/"):
        for file in files:
            if file.endswith(".yaml") and file != "dataset-spec.yaml":
                total_files += 1
                if validate_yaml_file(os.path.join(root, file)):
                    valid_files += 1
    print(f"\nValidation complete: {valid_files}/{total_files} files are valid.")

if __name__ == "__main__":
    validate_all_yaml_files()