class ConfigMissingFieldError(Exception):
    def __init__(self, field: str, child: "ConfigMissingFieldError" = None):
        if child is None:
            self.field_list = [field]
        else:
            self.field_list = [field] + child.field_list

    def __str__(self):
        return f"missing field '{' -> '.join(self.field_list)}'"
