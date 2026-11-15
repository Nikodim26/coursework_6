import secrets
from config import settings
from users.models import User
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.views.generic import CreateView, TemplateView, ListView
from customer_management.models import Customer
from mailing_management.models import NewsLetter
from users.forms import UserRegisterForm
from django.contrib.auth.mixins import LoginRequiredMixin

from users.services import access_manager


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

    def post(self, request, *args, **kwargs):
        for user in self.get_queryset():
            user.is_active = (request.POST.get(f'is_active_{user.id}') != 'True')
            user.save()
        return redirect('users:home')

    def dispatch(self, request, *args, **kwargs):
        response = access_manager(self,request, 'Доступ только для суперпользователей и менеджеров.')
        return super().dispatch(request, *args, **kwargs) if not response else response