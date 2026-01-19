from rest_framework import permissions
from .models import Resurs, AccessLvl

class HasAccess(permissions.BasePermission):
    def has_permission(self, request, view):

        print("Пользователь:", getattr(request.user, 'email', 'Аноним'))
        if '/api/products/' in request.path:
            resurs_name = 'products'
        elif '/api/orders/' in request.path:
            resurs_name = 'orders'
        elif '/api/users/' in request.path:
            resurs_name = 'users'
        else: 
            return False
        
        try:
            resurs = Resurs.objects.get(name = resurs_name)
        except Resurs.DoesNotExist:
            print("Ресурс не найден")
            return False
        
        user_roles = request.user.userrole_set.values_list('role_id', flat = True)
        print("ID ролей пользователя:", list(user_roles))

        rule = AccessLvl.objects.filter(
            role_id__in = user_roles,
            resurs = resurs
        ).first()

        if not rule:
            print("Правило не найдено")
            return False
        
        if request.method == 'GET' and rule.can_read:
            return True
        if request.method == 'POST' and rule.can_create:
            return True
        if request.method in ['PUT', 'PATCH'] and rule.can_update:
            return True
        if request.method == 'DELETE' and rule.can_delete:
            return True
        
        print("Метод не разрешён")
        return False