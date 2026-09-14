"""足し算のサンプルモジュール。"""


def sample_add(a: int, b: int) -> int:
    """2 つの整数の和を返す。

    Args:
        a (int): 1 つ目の整数。
        b (int): 2 つ目の整数。

    Raises:
        TypeError: a または b が整数でない場合。

    Returns:
        int: a と b の和。

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
