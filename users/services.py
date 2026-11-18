from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render

LIST_TEMPLATES = ['customer.html', 'letter.html', 'newsletter.html']

EDIT_TEMPLATES = [
    'create_update_customer.html', 'customer_delete_form.html',
    'create_update_letter.html', 'letter_delete_form.html',
    'create_update_mail.html', 'newsletter_delete_form.html',
]


def access_manager(obj, request, message):
    user = request.user

    if not user.is_authenticated:
        return None

    is_manager = user.groups.filter(name="Менеджеры").exists()
    is_super = user.is_superuser

    if obj.template_name in LIST_TEMPLATES:
        is_host = obj.get_object().owner_id == user.id
        if not (is_manager or is_super or is_host):
            return _denied(request, message)

    if obj.template_name == 'users.html':
        if not (is_manager or is_super):
            return _denied(request, message)

    if obj.template_name in EDIT_TEMPLATES:
        if is_manager:
            return _denied(request, message)

    return None


def _denied(request, message):
    return render(request, 'permission_denied.html', {
        'message': message,
        'error': 'Ошибка 403 Forbidden'
    }, status=403)


class ProtectedView(LoginRequiredMixin):
    access_message = 'Доступ запрещён'

    def dispatch(self, request, *args, **kwargs):
        response = access_manager(self, request, self.access_message)
        if response:
            return response
        return super().dispatch(request, *args, **kwargs)
