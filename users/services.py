from django.shortcuts import render


def access_manager(obj,request,message):
    is_manager = request.user.groups.filter(name="Менеджеры").exists()
    is_super = request.user.is_superuser
    if not request.user.is_authenticated:
        return None

    if obj.template_name =='customer.html':
        obj_ = obj.get_object()
        is_host = obj_.owner_id == request.user.id

        if not (is_manager or is_super or is_host):
            return render(request, 'permission_denied.html', {
                'message': message,
                'error': 'Ошибка 403 Forbidden'
            }, status=403)

    if obj.template_name == 'users.html':

        if not (is_manager or is_super):
            return render(request, 'permission_denied.html', {
                'message': message,
                'error': 'Ошибка 403 Forbidden'
            }, status=403)
    return None