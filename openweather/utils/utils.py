def format_multiline_dunder_str(multiline_str: str) -> str:

    """
    Formats a multiline f-string of a class __str__ method into a Pythonic format.
    """

    return ", ".join((multiline_str).replace("\n", "").replace(" ", "").split(","))

def dataclass_dict_factory(data: dict) -> dict:
    return {x[0]: x[1] for x in data if x[0] not in ("_base_url", "_api_key")}
