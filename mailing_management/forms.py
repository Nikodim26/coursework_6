from django import forms

from mailing_management.models import NewsLetter


class MailingForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(MailingForm, self).__init__(*args, **kwargs)

        self.fields['start_time'].widget.attrs.update({
            'class': 'form-control border border-info custom-placeholder',
            'placeholder': 'ГГГГ-ММ-ДД ЧЧ:ММ:СС',
        })

        self.fields['end_time'].widget.attrs.update({
            'class': 'form-control border border-info custom-placeholder',
            'placeholder': 'ГГГГ-ММ-ДД ЧЧ:ММ:СС',
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