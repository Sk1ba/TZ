from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User, Role, Resurs, AccessLvl
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.hashers import check_password
from .permissions import HasAccess
from rest_framework.decorators import api_view

class RegisterView(APIView):
    def post(self, request):
        data = request.data
        email = data.get('email')
        password = data.get('password')
        password2 = data.get('password2')
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        patronymic = data.get('patronymic', '')

        if not email or not first_name or not last_name or not password:
            return Response({'error': 'Все поля обязательны'}, status=status.HTTP_400_BAD_REQUEST)
        
        if password != password2:
            return Response({'error': 'Пароли не совпадают'}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(email=email).exists():
            return Response({'error': 'Пользователь с таким email уже существует'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            patronymic=patronymic
        )

        return Response({'message': 'Регистрация успешна'}, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'error': 'Неверный email или пароль'}, status=status.HTTP_401_UNAUTHORIZED)

        if not user.is_active:
            return Response({'error': 'Аккаунт деактивирован'}, status=status.HTTP_401_UNAUTHORIZED)

        if not check_password(password, user.password):
            return Response({'error': 'Неверный email или пароль'}, status=status.HTTP_401_UNAUTHORIZED)

        refresh = RefreshToken.for_user(user)
        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'user': {
                'id': user.id,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
            }
        })
    
class DeleteAccountView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        user = request.user
        user.is_active = False
        user.save()
        return Response({'message': 'Акаунт успешно удален'}, status= status.HTTP_200_OK)
        
class ProfileUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        user = request.user
        data = request.data

        user.first_name = data.get('first_name', user.first_name)
        user.last_name = data.get('last_name', user.last_name)
        user.patronymic = data.get('patronymic', user.patronymic)
        user.save()

        return Response({
            'message': 'Профиль обновлён',
            'user': {
                'id': user.id,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'patronymic': user.patronymic,
            }
        }, status=status.HTTP_200_OK)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        return Response({'message': 'Вы успешно вышли из системы'}, status=status.HTTP_200_OK)
    
class ProductView(APIView):
    permission_classes = [IsAuthenticated, HasAccess]

    def get(self, request):
        return Response({'data': 'Список товаров'})
    
    def post(self, request):
        return Response({'message': 'Товар создан'})

@api_view(['POST'])
def manage_access_rule(request):
    if not request.user.is_admin:
        return Response({'error': 'Доступ запрещён'}, status=status.HTTP_403_FORBIDDEN)
    
    if not isinstance(request.data, dict):
        return Response({'error': 'Ожидался JSON объект'}, status=status.HTTP_400_BAD_REQUEST)

    role_name = request.data.get('role')
    resurs_name = request.data.get('resurs')

    if not role_name or not resurs_name:
        return Response({
            'error': 'Укажите роль и ресурс', 
            'получено': request.data
            }, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        role = Role.objects.get(name=role_name)
        resurs = Resurs.objects.get(name=resurs_name)
    except Role.DoesNotExist:
        return Response({'error': 'Роль не найдена'}, status=status.HTTP_400_BAD_REQUEST)
    except Resurs.DoesNotExist:
        return Response({'error': 'Ресурс не найдена'}, status=status.HTTP_400_BAD_REQUEST)

    rule, created = AccessLvl.objects.update_or_create(
        role=role,
        resurs=resurs,
        defaults={
            'can_read': request.data.get('can_read', False),
            'can_create': request.data.get('can_create', False),
            'can_update': request.data.get('can_update', False),
            'can_delete': request.data.get('can_delete', False),
        }
    )

    return Response({
        'message': 'Правило обновлено' if not created else 'Правило создано',
        'rule': {
            'role': role.name,
            'resurs': resurs.name,
            'can_read': rule.can_read,
            'can_create': rule.can_create,
            'can_update': rule.can_update,
            'can_delete': rule.can_delete,
        }
    }, status=status.HTTP_200_OK)


