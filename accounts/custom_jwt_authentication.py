from rest_framework_simplejwt.authentication import JWTAuthentication


class CustomJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        # Check if the request should bypass token authentication
        if self.should_bypass_authentication(request):
            return None
        return super().authenticate(request)

    def should_bypass_authentication(self, request):
        # Define criteria for bypassing token authentication
        skip_token_authentication = False

        # Check if the request path starts with any of the specified endpoints
        if (request.path.startswith('/sendOTP/') or
            request.path.startswith('/verifyOTP/') or
            request.path.startswith('/registerMember/') or
            request.path.startswith('/registerHead/') or
            # request.path.startswith('/POSTNewNotification/') or
            request.path.startswith('/api/token/refresh/')or
            request.path.startswith('/obtainToken/')):
            skip_token_authentication = True

        return skip_token_authentication
