from django.shortcuts import render

#simple flag that could be set from DB settings
MAINTENANCE_MODE = False


class MaintenanceMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

        
    
    def __call__(self, request):


        # check if the user is a superuser (admin)
        is_admin = request.user.is_authenticated and request.user.is_superuser
        
        # check if the app is in maintenance mode AND the user is NOT an admin
        if MAINTENANCE_MODE and not is_admin:
            # render a simple maintenance page
            return render(request, 'common/maintenance.html', status=503)

        # if not in maintenance or the user is an admin, proceed normally
        response = self.get_response(request)

        return response


