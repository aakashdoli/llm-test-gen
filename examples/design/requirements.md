# Requirements

## REQ-101: add(a:int, b:int) -> int
- Should handle negatives and zeros.
- Commutative property: add(a,b) == add(b,a).

## REQ-102: safe_divide(x:float, y:float) -> float
- Raise ValueError on y == 0.
- Preserve sign: safe_divide(-4,2) == -2.

## REQ-103: Math.square(n:int) -> int
- Non-negative for all integers.
- Large inputs within Python int range should not overflow.