from django.http import JsonResponse

CODE_MESSAGE_MAP = {
    200: 'OK.',
    400: 'Bad Request',
    405: 'Invalid method.',
    408: 'System is not able to process your request. Please try again.',
    500: 'Internal server error, please try again later',
}


class Response:
    def __init__(self, http_status):
        self.http_status = http_status
        self.http_message = CODE_MESSAGE_MAP[http_status]

    def resp(self, message=None):
        data = {'message': self.http_message}
        if message:
            data = message
        return JsonResponse(data=data, status=self.http_status)