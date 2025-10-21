import json
from django.http import JsonResponse
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError


def get_tokens_for_user(user):
    """Generate JWT tokens for a user"""
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


def get_user_from_token(request):
    """Extract user from JWT token in request"""
    try:
        from rest_framework_simplejwt.authentication import JWTAuthentication
        jwt_auth = JWTAuthentication()
        user, token = jwt_auth.authenticate(request)
        return user
    except:
        return None


def token_response(tokens, user_data=None):
    """Create a standardized token response"""
    response_data = {
        'access': tokens['access'],
        'refresh': tokens['refresh'],
    }
    if user_data:
        response_data['user'] = user_data
    return JsonResponse(response_data)


def error_response(message, status_code=400):
    """Create a standardized error response"""
    return JsonResponse({'error': message}, status=status_code)
