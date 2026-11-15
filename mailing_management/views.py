from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from mailing_management.forms import MailingForm
from mailing_management.models import NewsLetter
from users.services import access_manager


class NewsLettersView(LoginRequiredMixin,ListView):
    model = NewsLetter
    template_name = 'newsletters.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        is_manager = user.groups.filter(name="Менеджеры").exists()
        context['newsletters'] = NewsLetter.objects.all() if (user.is_superuser or is_manager) \
            else NewsLetter.objects.filter(owner=user)
        return context


class NewsLetterView(DetailView):
    model = NewsLetter
    template_name = 'newsletter.html'
    context_object_name = 'newsletter'
    pk_url_kwarg = 'pk'

    def dispatch(self, request, *args, **kwargs):
        response = access_manager(self, request, 'Не ты создавал - видеть запрещено!')
        return super().dispatch(request, *args, **kwargs) if not response else response

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        obj.update_status()
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recipients'] = self.object.recipients.all()
        return context


class NewsLetterCreateView(CreateView):
    model = NewsLetter
    form_class = MailingForm
    template_name = 'create_update_mail.html'
    success_url = reverse_lazy("mailing_management:newsletters")
    context_object_name = 'newsletter'

    def form_valid(self, form):
        NewsLetters = form.save(commit=False)
        NewsLetters.owner = self.request.user
        NewsLetters.save()
        return super().form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        response=access_manager(self, request, 'Ты просто менеджер - тебе Запрещено!')
        return super().dispatch(request, *args, **kwargs) if not response else response


class NewsLetterUpdateView(UpdateView):
    model = NewsLetter
    form_class = MailingForm
    template_name = 'create_update_mail.html'
    context_object_name = 'newsletter'

    def get_success_url(self):
        return self.object.get_absolute_url()

    def dispatch(self, request, *args, **kwargs):
        response=access_manager(self, request, 'Ты просто менеджер - тебе Запрещено!')
        return super().dispatch(request, *args, **kwargs) if not response else response


class NewsLetterDeleteView(DeleteView):
    model = NewsLetter
    template_name = 'newsletter_delete_form.html'
    success_url = reverse_lazy("mailing_management:newsletters")
    context_object_name = 'newsletter'

    def dispatch(self, request, *args, **kwargs):
        response=access_manager(self, request, 'Ты просто менеджер - тебе Запрещено!')
        return super().dispatch(request, *args, **kwargs) if not response else response