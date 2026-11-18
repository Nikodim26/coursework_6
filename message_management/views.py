from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.cache import cache
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from message_management.forms import LetterForm
from message_management.models import Letter
from users.services import ProtectedView


class LettersView(LoginRequiredMixin, ListView):
    model = Letter
    template_name = 'letters.html'
    context_object_name = 'letters'

    def get_queryset(self):
        user = self.request.user
        is_manager = user.groups.filter(name="Менеджеры").exists()
        if user.is_superuser or is_manager:
            return Letter.objects.all()
        return Letter.objects.filter(owner=user)


class LetterView(ProtectedView, DetailView):
    model = Letter
    template_name = 'letter.html'
    context_object_name = 'letter'
    pk_url_kwarg = 'pk'
    access_message = 'Не ты создавал — видеть запрещено!'


class LetterCreateView(ProtectedView, CreateView):
    model = Letter
    form_class = LetterForm
    template_name = 'create_update_letter.html'
    success_url = reverse_lazy("message_management:letters")
    context_object_name = 'letter'
    access_message = 'Ты просто менеджер — тебе запрещено!'

    def form_valid(self, form):
        letter = form.save(commit=False)
        letter.owner = self.request.user
        letter.save()
        return super().form_valid(form)


class LetterUpdateView(ProtectedView, UpdateView):
    model = Letter
    form_class = LetterForm
    template_name = 'create_update_letter.html'
    context_object_name = 'letter'
    access_message = 'Ты просто менеджер — тебе запрещено!'

    def get_success_url(self):
        return self.object.get_absolute_url()

    def form_valid(self, form):
        response = super().form_valid(form)

        cache.clear()
        return response


class LetterDeleteView(ProtectedView, DeleteView):
    model = Letter
    template_name = 'letter_delete_form.html'
    success_url = reverse_lazy("message_management:letters")
    context_object_name = 'letter'
    access_message = 'Ты просто менеджер — тебе запрещено!'
