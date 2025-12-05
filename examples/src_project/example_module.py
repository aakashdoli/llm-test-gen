"""Example module to demonstrate LLM TestGen."""

def add(a: int, b: int) -> int:
    """Return the sum of two integers."""
    return a + b

def safe_divide(x: float, y: float) -> float:
    """Divide x by y; raises ValueError for y==0."""
    if y == 0:
        raise ValueError("division by zero")
    return x / y

class Math:
    def square(self, n: int) -> int:
        """Return n^2."""
        return n * n
