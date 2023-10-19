from rest_framework.exceptions import ValidationError


# TODO: Refactor this mess
class ReadOnlyOrUnkownFieldErrorMixin:
    def validate(self, attrs):
        errors = []
        if hasattr(self, "initial_data"):
            unknown_keys = set(self.initial_data.keys()) - set(self.fields.keys())
            read_only_keys = []
            if hasattr(self.Meta, "read_only_fields"):
                read_only_keys = set(self.initial_data.keys()).intersection(
                    set(self.Meta.read_only_fields)
                )
            if read_only_keys:
                errors += [f"Got read_only fields: {read_only_keys}"]

            if unknown_keys:
                errors += [f"Got unknown fields: {unknown_keys}"]
            if errors:
                raise ValidationError(errors)
        return attrs
