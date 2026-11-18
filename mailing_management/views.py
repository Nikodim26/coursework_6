from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.cache import cache
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from mailing_management.forms import MailingForm
from mailing_management.models import NewsLetter
from users.services import ProtectedView


class NewsLettersView(LoginRequiredMixin, ListView):
    model = NewsLetter
    template_name = 'newsletters.html'
    context_object_name = 'newsletters'

    def get_queryset(self):
        user = self.request.user
        is_manager = user.groups.filter(name="Менеджеры").exists()
        if user.is_superuser or is_manager:
            return NewsLetter.objects.all()
        return NewsLetter.objects.filter(owner=user)


class NewsLetterView(ProtectedView, DetailView):
    model = NewsLetter
    template_name = 'newsletter.html'
    context_object_name = 'newsletter'
    pk_url_kwarg = 'pk'
    access_message = 'Не ты создавал — видеть запрещено!'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        obj.update_status()
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recipients'] = self.object.recipients.all()
        return context


class NewsLetterCreateView(ProtectedView, CreateView):
    model = NewsLetter
    form_class = MailingForm
    template_name = 'create_update_mail.html'
    success_url = reverse_lazy("mailing_management:newsletters")
    context_object_name = 'newsletter'
    access_message = 'Ты просто менеджер — тебе запрещено!'

    def form_valid(self, form):
        newsletter = form.save(commit=False)
        newsletter.owner = self.request.user
        newsletter.save()
        return super().form_valid(form)


class NewsLetterUpdateView(ProtectedView, UpdateView):
    model = NewsLetter
    form_class = MailingForm
    template_name = 'create_update_mail.html'
    context_object_name = 'newsletter'
    access_message = 'Ты просто менеджер — тебе запрещено!'

    def get_success_url(self):
        return self.object.get_absolute_url()

    def form_valid(self, form):
        response = super().form_valid(form)

        cache.clear()
        return response


class NewsLetterDeleteView(ProtectedView, DeleteView):
    model = NewsLetter
    template_name = 'newsletter_delete_form.html'
    success_url = reverse_lazy("mailing_management:newsletters")
    context_object_name = 'newsletter'
    access_message = 'Ты просто менеджер — тебе запрещено!'
