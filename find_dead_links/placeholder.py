def add_2(a: int) -> int:
    """Add 2 to the input integer."""
    return a + 2


if __name__ == "__main__":
    import random

    test_value = random.randint(1, 100)  # noqa: S311
    print(f"Adding 2 to {test_value} gives {add_2(test_value)}")  # noqa: T201
