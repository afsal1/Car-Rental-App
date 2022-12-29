"""
File Name: mixins.py
description: Define custom mixins
"""
from rest_framework import status
from rest_framework.response import Response


class HttpResponseMixin(object):
    """
    Class Name: ResponseViewMixin
    description: Define response formatting methods
    """

    @classmethod
    def success_response(self, code='HTTP_200_OK', message=None, data=None):
        """
        Function Name: success_response
        description: Return formatted success response
        Input:
        code - string - HTTP status code
        data - json - json data to be returned
        Output:
        Formatted json
        """

        return Response(
            headers={'status': getattr(status, code)},
            status=status.HTTP_200_OK,
            data={
                'message': message,
                'status': getattr(status, code),
                'data': data if not data is None else {}
            },
            content_type='application/json'
        )

    @classmethod
    def error_response(self, code=None, message=None, error=None):
        """
        Function Name: error_response
        description: Return formatted error response
        Input:
        code - string - HTTP status code
        data - json - json data to be returned
        Output:
        Formatted json
        """
        return Response(
            status=status.HTTP_400_BAD_REQUEST,
            data={
                'status': getattr(status, code),
                'message_list': message,
                'data': error
            },
            content_type='application/json'
        )

