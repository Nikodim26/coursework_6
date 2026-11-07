from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from mailing_list_management.models import NewsLetter
from message_management.forms import LetterForm
from message_management.models import Letter


class NewsLettersView(ListView):
    model = NewsLetter
    template_name = 'newsletters.html'
    context_object_name = 'newsletter'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['newsletters'] = NewsLetter.objects.all()
        return context


class NewsLetterView(DetailView):
    model = NewsLetter
    template_name = 'newsletter.html'
    context_object_name = 'newsletter'
    pk_url_kwarg = 'pk'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        obj.update_status()
        return obj


# class LetterCreateView(CreateView):
#     model = Letter
#     form_class = LetterForm
#     template_name = 'create_update_letter.html'
#     success_url = reverse_lazy("message_management:letters")
#     context_object_name = 'letter'
#
#
# class LetterUpdateView(UpdateView):
#     model = Letter
#     form_class = LetterForm
#     template_name = 'create_update_letter.html'
#     context_object_name = 'letter'
#
#     def get_success_url(self):
#         return self.object.get_absolute_url()
#
#
# class LetterDeleteView(DeleteView):
#     model = Letter
#     template_name = 'letter_delete_form.html'
#     success_url = reverse_lazy("message_management:letters")
#     context_object_name = 'letter'