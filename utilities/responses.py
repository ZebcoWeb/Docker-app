import json

from django.http import HttpResponse
from rest_framework import exceptions




class BaseResponce(HttpResponse):
    def send(self):
        status = self.__dict__.pop('status')
        rs_data = {
            'success': self.__dict__.pop('success'),
            'message': self.__dict__.pop('message'),
            'data': self.__dict__.pop('data'),
        }
        return HttpResponse(
            json.dumps(rs_data),
            status=status,
            content_type="application/json"
        )

class SuccessResponse(BaseResponce):
    def __init__(self, data=None, status=200, message=None):
        super().__init__()
        self.success = True
        self.status = status
        self.message = message
        self.data = data

class ErrorResponse(BaseResponce):
    def __init__(self, data=None, status=400, message=None):
        super().__init__()
        self.success = False
        self.status = status
        self.message = message
        self.data = data