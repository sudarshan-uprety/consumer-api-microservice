class ServerError(Exception):
    """Exception for Server Errors"""


class CustomException(Exception):
    """Exception for Already Exist"""

    def __init__(self, error_code, message, *args, **kwargs):
        self.error_code = error_code
        self.message = message
        return super(CustomException, self).__init__(*args, **kwargs)

