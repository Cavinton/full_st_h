from django.shortcuts import render, redirect
from .forms import UserProfileForm

from rest_framework import viewsets
from django.views.decorators.http import require_http_methods

from .models import UserProfile
from .serializers import UserProfileSerializer


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer


@require_http_methods(['POST'])
def user_profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST)
        if form.is_valid():
            user_profile = form.save(commit=False)
            user_profile.user = request.user
            user_profile.save()
            return redirect('appointment:appointment_list')  # замените на URL для записи к специалисту
    else:
        form = UserProfileForm()

    return render(request, 'user_profile.html', {'form': form})

'============================'

from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from drf_yasg.utils import swagger_auto_schema

from .serializers import RegisterSerializer

User = get_user_model()

class RegisterView(APIView):
    @swagger_auto_schema(request_body=RegisterSerializer())
    def post(self, request):
        data = request.data
        serializer = RegisterSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response('ВЫ успешно зарегистрировались', 201)
    

class ActivationView(APIView):
    def get(self, request, email, activation_code):
        user = User.objects.filter(email=email, activation_code=activation_code).first()
        if not user:
            return Response('Пользователь не найден', 494)
        user.activation_code = ''
        user.is_active = True
        user.save()
        return Response('Вы успешно активировали аккаунт', 200)
        