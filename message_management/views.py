from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from message_management.forms import LetterForm
from message_management.models import Letter
from users.services import access_manager


class LettersView(LoginRequiredMixin,ListView):
    model = Letter
    template_name = 'letters.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        is_manager = user.groups.filter(name="Менеджеры").exists()
        context['letters'] = Letter.objects.all() if (user.is_superuser or is_manager) \
            else Letter.objects.filter(owner=user)
        return context


class LetterView(DetailView):
    model = Letter
    template_name = 'letter.html'
    context_object_name = 'letter'
    pk_url_kwarg = 'pk'

    def dispatch(self, request, *args, **kwargs):
        response = access_manager(self, request, 'Не ты создавал - видеть запрещено!')
        return super().dispatch(request, *args, **kwargs) if not response else response



class LetterCreateView(CreateView):
    model = Letter
    form_class = LetterForm
    template_name = 'create_update_letter.html'
    success_url = reverse_lazy("message_management:letters")
    context_object_name = 'letter'

    def form_valid(self, form):
        Letter = form.save(commit=False)
        Letter.owner = self.request.user
        Letter.save()
        return super().form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        response=access_manager(self, request, 'Ты просто менеджер - тебе Запрещено!')
        return super().dispatch(request, *args, **kwargs) if not response else response


class LetterUpdateView(UpdateView):
    model = Letter
    form_class = LetterForm
    template_name = 'create_update_letter.html'
    context_object_name = 'letter'

    def get_success_url(self):
        return self.object.get_absolute_url()

    def dispatch(self, request, *args, **kwargs):
        response=access_manager(self, request, 'Ты просто менеджер - тебе Запрещено!')
        return super().dispatch(request, *args, **kwargs) if not response else response


class LetterDeleteView(DeleteView):
    model = Letter
    template_name = 'letter_delete_form.html'
    success_url = reverse_lazy("message_management:letters")
    context_object_name = 'letter'

    def dispatch(self, request, *args, **kwargs):
        response=access_manager(self, request, 'Ты просто менеджер - тебе Запрещено!')
        return super().dispatch(request, *args, **kwargs) if not response else response