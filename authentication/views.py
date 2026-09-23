from django.shortcuts import render, redirect

# Create your views here.
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.contrib.auth import get_user_model
from .serializers import UserRegistrationSerializer

User = get_user_model()

class UserRegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    
    permission_classes = [AllowAny]
    
    serializer_class = UserRegistrationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        return Response({
            "success": True,
            "message": "User registered successfully!",
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "role": getattr(user, 'role', 'BUYER')
            }
        }, status=status.HTTP_201_CREATED)


from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .models import User

def register_ui_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered!")
            return redirect('register-ui')
            
        user = User.objects.create_user(username=username, email=email, password=password)
        login(request, user)
        messages.success(request, "Account successfully created!")
        return redirect('home')
        
    return render(request, 'authentication/register.html')

def login_ui_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        try:
            user_obj = User.objects.get(email=email)
            user = authenticate(request, username=user_obj.username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "Welcome back!")
                return redirect('home')
            else:
                messages.error(request, "Wrong Password!")
        except User.DoesNotExist:
            messages.error(request, "This email is not registered!")
            
    return render(request, 'authentication/login.html')

def logout_ui_view(request):
    logout(request)
    messages.info(request, "You logout the account.")
    return redirect('home')