from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView

from customer_management.models import Customer
from mailing_management.models import NewsLetter
from message_management.forms import LetterForm
from message_management.models import Letter

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


class LettersView(ListView):
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