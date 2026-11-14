import secrets

from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.views.generic import CreateView, TemplateView, ListView

from config import settings
from customer_management.models import Customer
from mailing_management.models import NewsLetter
from users.forms import UserRegisterForm

from users.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages


class UserCreateView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'login_register.html'
    success_url = reverse_lazy("users:login_")

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        token = secrets.token_hex(16)
        user.token = token
        user.save()

        # Правильная генерация ссылки
        url = self.request.build_absolute_uri(
            reverse('users:email-confirm', kwargs={'token': token})
        )

        send_mail(
            subject="Подтверждение почты",
            message=f"Привет! Перейди по ссылке, чтобы подтвердить почту: {url}",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email],
            fail_silently=False,
        )

        self.object = user
        return HttpResponseRedirect(self.get_success_url())


def email_verification(request, token):
    user = get_object_or_404(User, token=token)

    user.is_active = True
    user.token = ''
    user.save()

    return redirect(reverse('users:login'))


class HomeView(TemplateView):
    template_name = 'start_mailing.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        now = timezone.now()

        active_newsletters = NewsLetter.objects.filter(
            status='Запущена'
        ) | NewsLetter.objects.filter(
            start_time__lte=now,
            end_time__gte=now
        )

        context['active_newsletters_count'] = active_newsletters.count()
        context['all_newsletters_count'] = NewsLetter.objects.count()
        context['customers_count'] = Customer.objects.count()
        return context


class IntermediateView(TemplateView):
    template_name = 'intermediate.html'


class UsersListView(LoginRequiredMixin, ListView):
    model = User
    template_name = 'users.html'
    context_object_name = 'users'

    def get_queryset(self):
        return User.objects.filter(is_superuser=False).exclude(groups__name="Менеджеры")

    def dispatch(self, request, *args, **kwargs):
        is_manager = request.user.groups.filter(name="Менеджеры").exists()

        if not (is_manager or request.user.is_superuser):
            return render(request, 'permission_denied.html', {
                'message': 'Доступ к этому разделу есть только у суперпользователей и менеджеров.',
                'error': 'Ошибка 403 Forbidden («Запрещено»)'
            }, status=403)

        return super().dispatch(request, *args, **kwargs)


    def post(self, request, *args, **kwargs):
        users = self.get_queryset()

        for user in users:
            key = f'is_active_{user.id}'
            user.is_active = (request.POST.get(key) != 'True')
            user.save()

        messages.success(request, 'Настройки сохранены')
        return redirect('users:home')
