from django import forms
from .models import *
from django.contrib.admin.widgets import AdminDateWidget
from django.core.exceptions import ValidationError


class OrderCreateForm(forms.Form):
    id = forms.IntegerField(label='номер заказа')
    date_start = forms.DateField(label='дата начала проживания', widget=AdminDateWidget)
    date_stop = forms.DateField(label='дата окончания проживания', widget=AdminDateWidget)
    order_client = forms.ModelChoiceField(label='клиент', queryset=Client.objects.all())
    order_bed = forms.ModelChoiceField(label='комната', queryset=Bed.objects.all())

    def save(self):
        new_order = Order.objects.create(
            date_start=self.cleaned_data['date_start'],
            date_stop=self.cleaned_data['date_stop'],
            order_client=self.cleaned_data['order_client'],
            order_bed=self.cleaned_data['order_bed']
        )
        return new_order


class OrderEditForm(forms.Form):
    id = forms.IntegerField(label='номер заказа')
    date_start = forms.DateField(label='дата начала проживания', widget=AdminDateWidget)
    date_stop = forms.DateField(label='дата окончания проживания', widget=AdminDateWidget)
    order_client = forms.ModelChoiceField(label='клиент', queryset=Client.objects.all())
    order_bed = forms.ModelChoiceField(label='комната', queryset=Bed.objects.all())

    id.widget.attrs.update({'readonly': 'readonly'})

    def update(self, idi):
        re_order = Order.objects.get(id=idi)
        re_order.order_client = self.cleaned_data['order_client']
        re_order.order_bed = self.cleaned_data['order_bed']
        re_order.date_start = self.cleaned_data['data_start']
        re_order.date_stop = self.cleaned_data['data_stop']
        re_order.save()
        return re_order
