"""
Schema constraints and validation
"""

# Custom Exceptions
class PrimaryKeyViolation(Exception):
    pass

class UniqueConstraintViolation(Exception):
    pass

class NotNullViolation(Exception):
    pass

class Schema:
    def __init__(self):
        self.fields = {}           # field_name -> rule dict
        self.primary_key = None
        self.unique_fields = set()
        self.not_null_fields = set()

    def add_field(self, name, field_type, primary_key=False, unique=False, not_null=False, default=None, required=False):
        """
        Add a field with constraints.
        """
        if primary_key:
            if self.primary_key:
                raise ValueError("Only one primary key allowed.")
            self.primary_key = name
            unique = True      # Primary key is always unique
            not_null = True    # Primary key is always not null

        self.fields[name] = {
            "type": field_type,
            "primary_key": primary_key,
            "unique": unique,
            "not_null": not_null,
            "default": default,
            "required": required
        }

        if unique:
            self.unique_fields.add(name)
        if not_null:
            self.not_null_fields.add(name)

    def validate(self, record: dict, dataset: list):
        """
        Validate a record against schema rules and constraints.
        """
        # Type, required, and default checks
        for field, rule in self.fields.items():
            value = record.get(field)

            if rule.get("required") and field not in record:
                raise ValueError(f"Missing required field: {field}")

            if field in record and value is not None and not isinstance(value, rule["type"]):
                raise TypeError(f"{field} must be {rule['type'].__name__}")

            if "default" in rule and value is None:
                record[field] = rule["default"]

        # Not Null check
        for field in self.not_null_fields:
            if field not in record or record[field] is None:
                raise NotNullViolation(f"Field '{field}' cannot be null.")

        # Primary Key check
        if self.primary_key:
            pk_value = record.get(self.primary_key)
            for existing in dataset:
                if existing.get(self.primary_key) == pk_value:
                    raise PrimaryKeyViolation(
                        f"Primary key '{self.primary_key}' with value '{pk_value}' already exists."
                    )

        # Unique check (excluding primary key)
        for field in self.unique_fields:
            if field == self.primary_key:
                continue
            value = record.get(field)
            if value is not None:
                for existing in dataset:
                    if existing.get(field) == value:
                        raise UniqueConstraintViolation(
                            f"Duplicate value '{value}' for unique field '{field}'."
                        )

        return True
