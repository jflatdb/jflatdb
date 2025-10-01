"""
Schema constraints and validation
"""
class PrimaryKeyViolation(Exception):
    """Raised when a duplicate primary key value is inserted."""
    pass

class UniqueConstraintViolation(Exception):
    """Raised when a unique constraint is violated."""
    pass

class NotNullViolation(Exception):
    """Raised when a not-null field is missing or None."""
    pass

class Schema:
    def __init__(self):
        self.rules = {}
        self.primary_key = None

     def define(self, rules: dict):
        """
        Define schema rules.
        Example:
        schema.define({
            "id": {"type": int, "primary_key": True},
            "email": {"type": str, "unique": True},
            "name": {"type": str, "not_null": True}
        })
        """
        # Ensure only one primary key is defined
        for field, rule in rules.items():
            if rule.get("primary_key"):
                if self.primary_key is not None:
                    raise ValueError(f"Multiple primary keys not allowed (already set: {self.primary_key})")
                self.primary_key = field

        self.rules = rules

    def validate(self, record: dict, dataset: list = None):
        """
        Validate a record against schema rules and constraints.
        :param record: dict representing a single row/document
        :param dataset: list of existing rows/documents (for uniqueness checks)
        """
        dataset = dataset or []

        for field, rule in self.rules.items():
            value = record.get(field)

            # Required field check
            if rule.get("required") and field not in record:
                raise ValueError(f"Missing required field: {field}")

            # Not Null constraint
            if rule.get("not_null") and value is None:
                raise NotNullViolation(f"Field '{field}' cannot be null")

            # Type check
            if field in record and value is not None and not isinstance(value, rule["type"]):
                raise TypeError(f"{field} must be {rule['type'].__name__}, got {type(value).__name__}")

            # Default handling
            if "default" in rule and value is None:
                record[field] = rule["default"]

            # Primary Key constraint
            if rule.get("primary_key"):
                for row in dataset:
                    if row.get(field) == value:
                        raise PrimaryKeyViolation(f"Duplicate primary key '{value}' for field '{field}'")

            # Unique constraint
            if rule.get("unique"):
                for row in dataset:
                    if row.get(field) == value:
                        raise UniqueConstraintViolation(f"Duplicate unique value '{value}' for field '{field}'")

        return True  # ✅ Record passed validation