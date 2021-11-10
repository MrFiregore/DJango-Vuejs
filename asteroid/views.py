import json

from django.shortcuts import render
from rest_framework.exceptions import PermissionDenied
from django.http import HttpResponseNotFound, HttpResponse
from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    # Now add the HTTP status code to the response.
    if response is not None:
        response.data['status_code'] = response.status_code

    return response


# Create your views here.
from rest_framework import status

from asteroid.CustomResponse import CustomResponse


def index(request):
    return render(request, 'index.html', locals())


def error_400s(request, exception=None):
    return HttpResponse(content=json.dumps(CustomResponse([], status=status.HTTP_403_FORBIDDEN).data),
                        content_type="application/json")
