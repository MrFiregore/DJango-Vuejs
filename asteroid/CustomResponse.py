from rest_framework.response import Response
from rest_framework import status as code


class CustomResponse(Response):

    def __init__(self, data=None, status=code.HTTP_200_OK, headers=None,
                 exception=False, content_type=None):
        result = {
            'status': status,
            'data': data,
        }

        super(CustomResponse, self).__init__(data=result,
                                             headers=headers,
                                             status=status,
                                             exception=exception,
                                             content_type=content_type)
