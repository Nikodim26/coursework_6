from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from mailing_management.forms import MailingForm
from mailing_management.models import NewsLetter


class NewsLettersView(LoginRequiredMixin,ListView):
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


class NewsLetterUpdateView(UpdateView):
    model = NewsLetter
    form_class = MailingForm
    template_name = 'create_update_mail.html'
    context_object_name = 'newsletter'

    def get_success_url(self):
        return self.object.get_absolute_url()


class NewsLetterDeleteView(DeleteView):
    model = NewsLetter
    template_name = 'newsletter_delete_form.html'
    success_url = reverse_lazy("mailing_management:newsletters")
    context_object_name = 'newsletter'