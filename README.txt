Права доступа 

модели:

1. Роль
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

