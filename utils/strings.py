def is_positive(value):
    """
    Checks if a string can be a number and if its bigger than 0.
    """
    try:
        number_string = float(value)

    except ValueError:
        return False

    return number_string > 0
