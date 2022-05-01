def format_multiline_dunder_str(multiline_str: str) -> str:

    """
    Formats a multiline f-string of a class __str__ method into a Pythonic format.
    """

    return ", ".join((multiline_str).replace("\n", "").replace(" ", "").split(","))