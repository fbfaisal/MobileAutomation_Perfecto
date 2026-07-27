import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from libraries.ValidationManager import ValidationManager


validation = ValidationManager()


try:

    result = validation.validate_runtime_config()

    print("Runtime configuration validation passed:", result)


except Exception as error:

    print("Validation failed:")
    print(error)