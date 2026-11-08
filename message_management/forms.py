from django import forms

from message_management.models import Letter


class LetterForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(LetterForm, self).__init__(*args, **kwargs)

        self.fields['email_subject'].widget.attrs.update({
            'class': 'form-control border border-info custom-placeholder',
            'placeholder': 'Тема',
        })

        self.fields['letter_body'].widget.attrs.update({
            'class': 'form-control border border-warning bg-success p-2 text-dark bg-opacity-25 custom-placeholder',
            'placeholder': 'Содержание',
            'style': 'field-sizing: content;'
        })

    class Meta:
        model = Letter
        exclude = ['owner']