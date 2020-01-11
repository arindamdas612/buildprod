from django.forms import ModelForm
from django.forms import forms
from .models import Roll, Bag, Ship, ShipCart, PackingSlips

class RollForm(ModelForm):
    class Meta:
        model = Roll
        exclude = ('stock_timestamp', 'updated_timestamp')
    
    def __init__(self, *args, **kwargs):
        super(RollForm, self).__init__(*args, **kwargs)
        self.fields['seller'].widget.attrs\
            .update({
                'class': 'form-control'
            })
        self.fields['unit'].widget.attrs\
            .update({
                'class': 'form-control',
                'placeholder': 'Unit(s)',
            })
        self.fields['gsm'].widget.attrs\
            .update({
                'class': 'form-control mr-sm-4',
                'placeholder': 'GSM',
            })
        self.fields['color'].widget.attrs\
            .update({
                'class': 'form-control',
                'placeholder': 'Color',
            })
        self.fields['width'].widget.attrs\
            .update({
                'class': 'form-control',
                'placeholder': 'Width (in)',
            })
        self.fields['weight'].widget.attrs\
            .update({
                'class': 'form-control',
                'placeholder': 'Weight (kg)',
            })
        self.fields['length'].widget.attrs\
            .update({
                'class': 'form-control',
                'placeholder': 'Length (m)',
                'value': ''
            })
       
    

class BagForm(ModelForm):
    class Meta:
        model = Bag
        exclude = ('status', 'weight', 'create_timestamp', 'updated_timestamp')
    
    def __init__(self, *args, **kwargs):
        self.roll_weight = kwargs.pop('roll_weight', None)
        self.waste_weight = kwargs.pop('waste_weight', None)
        super(BagForm, self).__init__(*args, **kwargs)
        self.fields['roll'].widget.attrs\
            .update({
                'class': 'form-control'
            })
        self.fields['bag_type'].widget.attrs\
            .update({
                'class': 'form-control'
            })
        self.fields['height'].widget.attrs\
            .update({
                'class': 'form-control',
                'placeholder': 'height (in)',
            })
        self.fields['width'].widget.attrs\
            .update({
                'class': 'form-control',
                'placeholder': 'width (in)',
            })
        if self.instance:
            self.fields['roll'].queryset = Roll.objects.filter(unit__gt=0).order_by('color', 'gsm', 'width', 'weight')

    def clean(self):
        if not self.waste_weight:
            raise forms.ValidationError('Provide Waste Weight')
        if not self.roll_weight:
            raise forms.ValidationError('Provide Roll weight used for production')
        super().clean()
        




class ShipCartForm(ModelForm):
    class Meta:
        model = ShipCart
        exclude = ('cart_owner', 'create_timestamp')


    def __init__(self, *args, **kwargs):
        super(ShipCartForm, self).__init__(*args, **kwargs)
        self.fields['bag'].widget.attrs\
            .update({
                'class': 'form-control'
            })
        self.fields['weight'].widget.attrs\
            .update({
                'class': 'form-control',
                'placeholder': 'Shipment weight'
            })
        self.fields['pricing'].widget.attrs\
            .update({
                'class': 'form-control'
            })
        if self.instance:
            self.fields['bag'].queryset = Bag.objects.filter(weight__gt=0, status='stocked')
    
    def clean(self):
        super().clean()
        data = self.cleaned_data
        if data['weight'] > data['bag'].weight:
            raise forms.ValidationError('Shippment weight cannot excced bag weight')
        
    
    def save(self, user):
        obj = super().save(commit = False)
        obj.cart_owner = user
        obj.save()
        return obj

class PackingSlipForm(ModelForm):
    class Meta:
        model = PackingSlips
        exclude = ('basic_weight', 'color_weight', 'basic_amount', 'color_amount', 'total_amount', 'prepared_by', 'create_timestamp')


    def __init__(self, *args, **kwargs):
        super(PackingSlipForm, self).__init__(*args, **kwargs)
        self.fields['party'].widget.attrs\
            .update({
                'class': 'form-control',
            })
        self.fields['basic_rate'].widget.attrs\
            .update({
                'class': 'form-control',
                'placeholder': 'Basic rate per Kg',
            })
        self.fields['color_rate'].widget.attrs\
            .update({
                'class': 'form-control',
                'placeholder': 'Color rate per Kg',
            })
        self.fields['print_amount'].widget.attrs\
            .update({
                'class': 'form-control',
                'placeholder': 'Printing Charges',
            })
        self.fields['fare_amount'].widget.attrs\
            .update({
                'class': 'form-control',
                'placeholder': 'Fare Charges',
            })
        self.fields['advance_amount'].widget.attrs\
            .update({
                'class': 'form-control',
                'placeholder': 'Advance (if any)',
            })
    
    def save(self, user):
        obj = super().save(commit = False)
        obj.prepared_by = user
        obj.save()
        return obj
