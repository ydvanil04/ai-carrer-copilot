class InvalidProfileError(Exception):
    """Raised when a required profile field is missing or blank.

    This exception is used in validators.py when a field such as
    'name' or 'current_role' is absent from the user's profile or
    contains only whitespace.
    """
    pass


class UnknownRoleError(Exception):
    """Raised when the selected target role is not found in job_roles.json.

    This exception is used in career_engine.py when the role key
    provided by the user does not match any entry in the loaded
    job roles data file.
    """
    pass


class InvalidExperienceError(Exception):
    """Raised when years of experience is negative or non-numeric.

    This exception is used in validators.py when the value supplied
    for years of experience cannot be interpreted as a non-negative
    number (e.g. a string like 'abc' or a negative integer such as -1).
    """
    pass
