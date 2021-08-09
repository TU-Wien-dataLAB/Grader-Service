from typing import Optional, Any
import os
import json

class InvalidEntry(ValueError):
    pass


class MissingEntry(ValueError):
    pass

class Gradebook:
    """
    The gradebook object to interface with the JSON output file of a conversion.
    Should only be used as a context manager when changing the data.
    """
    def __init__(self, dest_json: str) -> None:
        self.json_file: str = dest_json
        if os.path.isfile(self.json_file):
            with open(self.json_file, "r") as f:
                self.data: dict = json.load(f)
        else:
            os.makedirs(os.path.dirname(self.json_file), exist_ok=True)
            self.data: dict = dict()
            with open(self.json_file, "w") as f:
                json.dump(self.data, f)
    
    def __enter__(self) -> 'Gradebook':
        return self
    
    def __exit__(self, exc_type: Optional[Any], exc_value: Optional[Any], traceback: Optional[Any]) -> None:
        with open(self.json_file, "w") as f:
            json.dump(self.data, f)
    
    