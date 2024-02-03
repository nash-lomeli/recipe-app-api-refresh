from rest_framework.exceptions import APIException


class ProfileDoesNotExist(APIException):
    """Custom exception triggered by Core.exceptions"""
    status_code=400
    default_detail = 'The requested profile does not exist.'
