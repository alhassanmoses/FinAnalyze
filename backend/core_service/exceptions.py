"""Custom Exceptions"""


from fastapi import HTTPException


class InvalidId(Exception):
    """Raised when trying to create an ObjectId from invalid data."""


class CurrentUserNotFound(HTTPException):
    """Raised when a request to a protected route fails to retrived the active user"""


class NoneOwnerPermissionDenied(HTTPException):
    """Raised when a request is made to a protected route using someone elses ID"""
