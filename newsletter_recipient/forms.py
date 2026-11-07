from django import forms

from newsletter_recipient.models import Customer


class CustomerForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CustomerForm, self).__init__(*args, **kwargs)

        self.fields['fio'].widget.attrs.update({
            'class': 'form-control border border-info',
            'placeholder': 'Иванов Иван Иванович',
        })

        self.fields['email'].widget.attrs.update({
            'class': 'form-control border border-info',
        })

        self.fields['description'].widget.attrs.update({
            'class': 'form-control border border-warning bg-success p-2 text-dark bg-opacity-25 custom-placeholder',
            'placeholder': 'Примечание',
            'style': 'height: 150px;'
        })

    class Meta:
        model = Customer
        exclude = ['owner']