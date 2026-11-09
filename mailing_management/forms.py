from django import forms
from django.utils import timezone

from mailing_management.models import NewsLetter


class MailingForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(MailingForm, self).__init__(*args, **kwargs)

        self.fields['start_time'].widget.attrs.update({
            'class': 'form-control border border-info custom-placeholder',
        })

        self.fields['end_time'].widget.attrs.update({
            'class': 'form-control border border-info custom-placeholder',
        })

        self.fields['message'].widget.attrs.update({
            'class': 'form-control border border-info',
        })

        self.fields['recipients'].widget.attrs.update({
            'class': 'form-control border border-info',
        })

    class Meta:
        model = NewsLetter
        exclude = ['status']
        widgets = {
            'start_time': forms.DateTimeInput(
                attrs={'type': 'datetime-local', 'step': 1},
                format='%Y-%m-%dT%H:%M:%S',
            ),
            'end_time': forms.DateTimeInput(
                attrs={'type': 'datetime-local', 'step': 1},
                format='%Y-%m-%dT%H:%M:%S',
            ),
        }

    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')

        now = timezone.now()

        if start_time and start_time < now:
            self.add_error('start_time', 'Время запуска не может быть в прошлом.')

        if start_time and end_time:
            if start_time >= end_time:
                self.add_error('end_time', 'Время окончания должно быть строго позже времени запуска.')

        return cleaned_data
