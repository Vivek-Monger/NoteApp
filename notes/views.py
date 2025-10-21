from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import (
    ListView, CreateView, UpdateView, DeleteView
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Note
from .forms import UserRegistrationForm, NoteForm
from .utils import get_tokens_for_user, token_response, error_response


class CustomLoginView(LoginView):
    template_name = 'login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('note_list')

    @csrf_exempt
    def post(self, request, *args, **kwargs):
        # Check if it's an API request (JSON)
        if request.content_type == 'application/json':
            try:
                import json
                data = json.loads(request.body)
                username = data.get('username')
                password = data.get('password')
                
                if username and password:
                    user = authenticate(username=username, password=password)
                    if user and user.is_active:
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
        else:
            # Regular form submission
            return super().post(request, *args, **kwargs)


@csrf_exempt
def register_view(request):
    if request.method == 'POST':
        # Check if it's an API request (JSON)
        if request.content_type == 'application/json':
            try:
                import json
                data = json.loads(request.body)
                form = UserRegistrationForm(data)
                if form.is_valid():
                    user = form.save()
                    tokens = get_tokens_for_user(user)
                    return token_response(tokens, {
                        'id': user.id,
                        'username': user.username,
                        'email': user.email
                    })
                else:
                    return error_response('Registration failed', 400)
            except Exception as e:
                return error_response('Invalid JSON data', 400)
        else:
            # Regular form submission
            form = UserRegistrationForm(request.POST)
            if form.is_valid():
                user = form.save()
                username = form.cleaned_data.get('username')
                messages.success(request, f'Account created for {username}!')
                login(request, user)
                return redirect('note_list')
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})


@csrf_exempt
def logout_view(request):
    # Check if it's an API request (JSON)
    if request.content_type == 'application/json':
        try:
            import json
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
    else:
        # Regular logout
        logout(request)
        messages.info(request, 'You have been logged out.')
        return redirect('login')


@csrf_exempt
@require_http_methods(["POST"])
def refresh_token_view(request):
    """Refresh JWT access token"""
    try:
        import json
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


class NoteListView(LoginRequiredMixin, ListView):
    model = Note
    template_name = 'note_list.html'
    context_object_name = 'notes'
    paginate_by = 10

    def get_queryset(self):
        return Note.objects.filter(author=self.request.user)


class NoteCreateView(LoginRequiredMixin, CreateView):
    model = Note
    form_class = NoteForm
    template_name = 'note_form.html'
    success_url = reverse_lazy('note_list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, 'Note created successfully!')
        return super().form_valid(form)


class NoteUpdateView(LoginRequiredMixin, UpdateView):
    model = Note
    form_class = NoteForm
    template_name = 'note_form.html'
    success_url = reverse_lazy('note_list')

    def get_queryset(self):
        return Note.objects.filter(author=self.request.user)

    def form_valid(self, form):
        messages.success(self.request, 'Note updated successfully!')
        return super().form_valid(form)


class NoteDeleteView(LoginRequiredMixin, DeleteView):
    model = Note
    template_name = 'note_confirm_delete.html'
    success_url = reverse_lazy('note_list')

    def get_queryset(self):
        return Note.objects.filter(author=self.request.user)

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Note deleted successfully!')
        return super().delete(request, *args, **kwargs)
