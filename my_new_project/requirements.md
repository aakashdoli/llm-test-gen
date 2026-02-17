# PrimeMart Requirements

## REQ-001: Auth Logic (models.py)
- `validate_user(email, password)`: Should return user dict if credentials match, else None.
- `create_user`: Should raise DuplicateKeyError if email already exists.

## REQ-002: Product Management (models.py)
- `create_product`: Price must be a non-negative float.
- `update_product`: Should only update fields that are not None.
- `delete_product`: If `soft=True`, it should set `is_active=False` instead of removing data.

## REQ-003: Cart Logic (models.py)
- `add_to_cart`: If `qty` is <= 0, it should default to 1.
- `update_cart_item`: If `qty` is <= 0, the item should be removed from the cart entirely.
- `get_cart`: Should return an empty cart structure if the user has no cart yet.

## REQ-004: Buying (routes/product.py)
- Only users with role="user" can buy products.
- Retailers cannot buy products.