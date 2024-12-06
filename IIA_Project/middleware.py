from django.http import JsonResponse
from django.db import OperationalError

class DatabaseErrorMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            response = self.get_response(request)
            print("CHECKING DATABSE")
        except OperationalError as e:
            print(f"OperationalError caught in middleware: {e}")
            return JsonResponse(
                {'error': 'Database connection is unavailable. Please try again later.'},
                status=503
            )
        except Exception as e:
            # Catch other exceptions if necessary
            print(f"Unexpected error in middleware: {e}")
            return JsonResponse({'error': 'Internal Server Error'}, status=500)
        return response
