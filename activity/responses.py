from django.http import JsonResponse

CODE_MESSAGE_MAP = {
    200: 'OK.',
    402: 'Params missing in request',
    405: 'Invalid method.',
    408: 'System is not able to process your request. Please try again.',
    500: 'Internal server error, please try again later',
}


class Response:
    def __init__(self, http_status):
        self.http_status = http_status
        self.message = CODE_MESSAGE_MAP[http_status]

    def resp(self):
        return JsonResponse(data={'message': self.message}, status=self.http_status)