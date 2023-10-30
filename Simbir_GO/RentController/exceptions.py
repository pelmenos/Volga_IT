from rest_framework import status
from rest_framework.exceptions import APIException


class NotSpecified(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Item must be specified'
    default_code = 'not_specified'
