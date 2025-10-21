class DatabaseError(Exception):
    """Raised for database-related errors."""
    pass

class NotFoundError(Exception):
    """Raised when a resource is not found."""
    pass