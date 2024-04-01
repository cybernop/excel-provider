from excel_provider.error.config_missing_field_error import ConfigMissingFieldError


def test_config_missing_field_error_simple():
    error = ConfigMissingFieldError("test_field")
    assert str(error) == "missing field 'test_field'"


def test_config_missing_field_error_parent():
    child = ConfigMissingFieldError("test_field")
    error = ConfigMissingFieldError("parent_field", child)
    assert str(error) == "missing field 'parent_field -> test_field'"
