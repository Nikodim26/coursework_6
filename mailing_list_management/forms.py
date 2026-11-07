from django import forms

from mailing_list_management.models import NewsLetter


class MailingListForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(MailingListForm, self).__init__(*args, **kwargs)

        self.fields['start_time'].widget.attrs.update({
            'class': 'form-control border border-info custom-placeholder',
            'placeholder': 'ГГГГ-ММ-ДД ЧЧ:ММ:СС',
        })

        self.fields['end_time'].widget.attrs.update({
            'class': 'form-control border border-info custom-placeholder',
            'placeholder': 'ГГГГ-ММ-ДД ЧЧ:ММ:СС',
        })


    class Meta:
        model = NewsLetter
        exclude = ['owner']