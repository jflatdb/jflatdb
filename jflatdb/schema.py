"""
Schema constraints and validation
"""

class Schema:
    def __init__(self):
        self.rules = {}

    def define(self, rules: dict):
        self.rules = rules

    def validate(self, record: dict):
        for field, rule in self.rules.items():
            if rule.get("required") and field not in record:
                raise ValueError(f"Missing required field: {field}")
            if field in record:
                if not isinstance(record[field], rule["type"]):
                    raise TypeError(f"{field} must be {rule['type'].__name__}")
                if "default" in rule and not record.get(field):
                    record[field] = rule["default"]
