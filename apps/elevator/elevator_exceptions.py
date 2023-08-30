##############
# Libraries #
##############

from fastapi import HTTPException, status

from typing import Optional


###########################
# Server error exception #
###########################

class ServerError(HTTPException):
    def __init__(self, message: str, original_exception: Optional[Exception] = None):
        super().__init__(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                         detail=message,
                         headers={"X-Error": "ServerError"})
        self.original_exception = original_exception


###########################
# Database error exception #
###########################

class DatabaseError(HTTPException):
    def __init__(self, message: str, original_exception: Optional[Exception] = None):
        super().__init__(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                         detail=message,
                         headers={"X-Error": "DBError"})
        self.original_exception = original_exception
