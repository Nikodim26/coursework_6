from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView

from customer_management.models import Customer
from mailing_management.models import NewsLetter
from message_management.forms import LetterForm
from message_management.models import Letter


class LettersView(LoginRequiredMixin,ListView):
    model = Letter
    template_name = 'letters.html'
    context_object_name = 'letters'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['letters'] = Letter.objects.all()
        return context


class LetterView(DetailView):
    model = Letter
    template_name = 'letter.html'
    context_object_name = 'letter'
    pk_url_kwarg = 'pk'


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


class LetterUpdateView(UpdateView):
    model = Letter
    form_class = LetterForm
    template_name = 'create_update_letter.html'
    context_object_name = 'letter'

    def get_success_url(self):
        return self.object.get_absolute_url()


class LetterDeleteView(DeleteView):
    model = Letter
    template_name = 'letter_delete_form.html'
    success_url = reverse_lazy("message_management:letters")
    context_object_name = 'letter'