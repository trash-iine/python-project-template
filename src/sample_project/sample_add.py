"""Sample Add module."""


def sample_add(a: int, b: int) -> int:
    """Return the sum of two integers.

    Args:
        a (int): First integer.
        b (int): Second integer.

    Raises:
        TypeError: If a or b is not an integer.

    Returns:
        int: The sum of a and b.

    Examples:
        >>> sample_add(2, 3)
        5
        >>> sample_add(-1, 1)
        0
        >>> sample_add("2", 3)
        Traceback (most recent call last):
            ...
        TypeError: Invalid types: a=<class 'str'>, b=<class 'int'>

    """
    if not isinstance(a, int) or not isinstance(b, int):
        msg = f"Invalid types: a={type(a)}, b={type(b)}"
        raise TypeError(msg)

    return a + b
