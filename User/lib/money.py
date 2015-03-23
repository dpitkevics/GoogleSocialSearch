

def convert_to_money(number):
    """
    always:
    - shows 2 decimal places
    - shows thousands separator if necessary
    - retains integrity of original var for later re-use
    - allows for concise calling
    """
    import math

    try:
        return str(format(math.floor(number * 100) / 100, ',.2f'))
    except TypeError:
        return str(format(math.floor(0 * 100) / 100, ',.2f'))