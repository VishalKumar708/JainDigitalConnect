from rest_framework_simplejwt.tokens import AccessToken
import logging

error_logger = logging.getLogger('error')
info_logger = logging.getLogger('info')


def get_user_id_from_token_view(request):
    # Get the Authorization header from the request
    authorization_header = request.META.get("HTTP_AUTHORIZATION")

    if authorization_header:
        # Check if the header starts with "Bearer "
        if authorization_header.startswith("Token "):
            # Extract the token (remove "Bearer " from the header)
            token_string = authorization_header[len("Token "):].strip()

            try:
                # Decode the access token
                token = AccessToken(token_string)

                # to print all payload data inside "access token"
                # print("complete payload data==> ",token.payload.items())

                # Access the user_id claim from the token's payload
                user_id = token.payload.get('user_id')

                if user_id is not None:
                    # Return the user_id in the response
                    return user_id
                else:
                    return None

            except Exception as e:
                # Handle token decoding or validation errors
                error_logger.error("An exception occurred when we find user_id by access token. %s", str(e))
