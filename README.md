Система разграничения прав доступа 

Аутентификация:
- Регистрация пользователя
- Вход по email и паролю (JWT)
- Обновление профиля
- Мягкое удаление аккаунта (`is_active = False`)
- Logout

Авторизация
- Проверка прав доступа к ресурсам
- 401 Unauthorized для неавторизованных
- 403 Forbidden для авторизованных без прав

Схема БД:
1. Пользователь
- email
- first_name
- last_name
- patronymic
- is_active
- is_admin

2. Роль
- id - перв ключ 
- name - роль (manager, admin, user)

2. Ресурс
- id - перв ключ
- name - ресурс (users, orders, products)

3. Уровень доступа 
- id
- role_id - внеш ключ на Роль
- element_id - внеш ключ на Ресурс
- can_read - возможность читать (bool)
- can_create - возможность создавать (bool)
- can_update - возможность обновлять (bool)
- can_delete - возможность удалять (bool)

4. Связь роли и пользователя 
- id 
- user_id - внеш ключ User
- role_id - внеш ключ Role

Thunder Client:

Аутентификация:
- POST /api/auth/register/ - регистрация
- POST /api/auth/login/ - вход
- POST /api/auth/logout/ - выход
- PUT /api/auth/profile/ - обновление профиля
- DELETE /api/auth/delete-account/ - удаление аккаунта

Авторизация:
- GET /api/products/