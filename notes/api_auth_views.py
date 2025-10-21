from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from .utils import get_tokens_for_user, token_response, error_response
from .forms import UserRegistrationForm
import json


@csrf_exempt
@require_http_methods(["POST"])
def api_register(request):
    """JWT API endpoint for user registration"""
    try:
        data = json.loads(request.body)
        # Convert password_confirm to password2 for Django form
        if 'password_confirm' in data:
            data['password2'] = data.pop('password_confirm')
        if 'password' in data:
            data['password1'] = data.pop('password')
            
        form = UserRegistrationForm(data)
        if form.is_valid():
            user = form.save()
            # Create Django session for web interface
            login(request, user)
            tokens = get_tokens_for_user(user)
            return token_response(tokens, {
                'id': user.id,
                'username': user.username,
                'email': user.email
            })
        else:
            # Return form errors for debugging
            errors = {}
            for field, field_errors in form.errors.items():
                errors[field] = [str(error) for error in field_errors]
            return JsonResponse({'error': 'Registration failed', 'details': errors}, status=400)
    except Exception as e:
        return error_response('Invalid JSON data', 400)


@csrf_exempt
@require_http_methods(["POST"])
def api_login(request):
    """JWT API endpoint for user login"""
    try:
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        
        if username and password:
            user = authenticate(request, username=username, password=password)
            if user and user.is_active:
                # Create Django session for web interface
                login(request, user)
                tokens = get_tokens_for_user(user)
                return token_response(tokens, {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email
                })
            else:
                return error_response('Invalid credentials', 401)
        else:
            return error_response('Username and password required', 400)
    except Exception as e:
        return error_response('Invalid JSON data', 400)


@csrf_exempt
@require_http_methods(["POST"])
def api_logout(request):
    """JWT API endpoint for user logout"""
    try:
        data = json.loads(request.body)
        refresh_token = data.get('refresh')
        if refresh_token:
            try:
                token = RefreshToken(refresh_token)
                token.blacklist()
                return JsonResponse({'message': 'Logout successful'})
            except Exception as e:
                return error_response('Invalid token', 400)
        else:
            return error_response('Refresh token required', 400)
    except Exception as e:
        return error_response('Invalid JSON data', 400)


@csrf_exempt
@require_http_methods(["POST"])
def api_refresh_token(request):
    """JWT API endpoint for token refresh"""
    try:
        data = json.loads(request.body)
        refresh_token = data.get('refresh')
        
        if refresh_token:
            try:
                token = RefreshToken(refresh_token)
                return JsonResponse({
                    'access': str(token.access_token),
                    'refresh': str(token)
                })
            except Exception as e:
                return error_response('Invalid refresh token', 401)
        else:
            return error_response('Refresh token required', 400)
    except Exception as e:
        return error_response('Invalid JSON data', 400)
