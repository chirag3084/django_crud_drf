class CorsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

        self.allowed_origins = ['http://localhost:3000']

    def __call__(self, request):
        response = self.get_response(request)
        origin = request
        origin = request.headers.get('Origin')
        
        if origin and origin in self.allowed_origins:
            # set the allowed origin header
            response["Access-Control-Allow-Origin"] = origin
            # set allowed methods (GET, POST, etc.)
            response["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
            # set allowed headers
            response["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
            # sllow cookies/credentials
            response["Access-Control-Allow-Credentials"] = "true"

        return response

    # handle preflight CORS requests (OPTIONS method)
    def process_request(self, request):
        if request.method == "OPTIONS" and "HTTP_ACCESS_CONTROL_REQUEST_METHOD" in request.META:
            response = self.get_response(request) # you must still call get_response
            
            # where you would handle the OPTIONS response headers if needed
            response["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
            response["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
            
            return response
        return None