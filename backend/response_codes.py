from enum import Enum

# Enum class for response codes and corresponding messages
class ResponseCodes(Enum):
    SUCCESS = {"code": 200, "message": "Success"}
    ORIGINAL_URL_ALREADY_EXISTS = {"code": 200, "message": "Original URL already exists"}
    SHORT_URL_ALREADY_EXISTS = {"code": 409, "message": "Short URL already exists"}
    NOT_FOUND = {"code": 404, "message": "Not found"}
    ERROR = {"code": 500, "message": "Error"}