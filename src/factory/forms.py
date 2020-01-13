from django.forms import ModelForm
from django.forms import forms
from .models import Roll, Bag, Ship, ShipCart, PackingSlips

class RollForm(ModelForm):
    class Meta:
        model = Roll
        exclude = ('print_type','stock_timestamp', 'updated_timestamp')
    
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
        exclude = ('print_type','status', 'weight', 'create_timestamp', 'updated_timestamp')
    
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
        exclude = ('bag', 'cart_owner', 'create_timestamp')


    def __init__(self, *args, **kwargs):
        self.bag = kwargs.pop('bag', None)
        super(ShipCartForm, self).__init__(*args, **kwargs)
        self.fields['weight'].widget.attrs\
            .update({
                'class': 'form-control',
                'placeholder': 'Shipment weight'
            })
        self.fields['bndl'].widget.attrs\
            .update({
                'class': 'form-control',
                'placeholder': 'number of BOSTA'
            })
        self.fields['remarks'].widget.attrs\
            .update({
                'class': 'form-control',
                'placeholder': 'Remarks'
            })
        self.fields['pricing'].widget.attrs\
            .update({
                'class': 'form-control'
            })
    
    def clean(self):
        super().clean()
        data = self.cleaned_data
        if data['weight'] > self.bag.weight:
            raise forms.ValidationError('Shippment weight cannot excced bag weight')
        
    
    def save(self, user):
        obj = super().save(commit = False)
        obj.cart_owner = user
        obj.bag = self.bag
        obj.save()
        return obj

class PackingSlipForm(ModelForm):
    class Meta:
        model = PackingSlips
        exclude = ('basic_weight', 'color_weight', 'wcut_weight', 'basic_amount', 'color_amount', 'wcut_amount', 'print_amount', 'block_amount', 'total_amount', 'prepared_by', 'create_timestamp')


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
        self.fields['wcut_rate'].widget.attrs\
            .update({
                'class': 'form-control',
                'placeholder': 'W-CUT rate per Kg',
            })
        self.fields['print_rate'].widget.attrs\
            .update({
                'class': 'form-control',
                'placeholder': 'Print Charges',
            })
        self.fields['block_rate'].widget.attrs\
            .update({
                'class': 'form-control',
                'placeholder': 'Block Charges',
            })
        self.fields['print_unit'].widget.attrs\
            .update({
                'class': 'form-control',
                'placeholder': 'Print Unit',
            })
        self.fields['block_unit'].widget.attrs\
            .update({
                'class': 'form-control',
                'placeholder': 'Block unit',
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


class FlexoPrintForm(ModelForm):
    class Meta:
        model = Roll
        exclude = ('seller', 'gsm', 'print_type', 'color', 'width', 'length', 'stock_timestamp', 'updated_timestamp')
    
    def __init__(self, *args, **kwargs):
        self.roll = kwargs.pop('roll', None)
        super(FlexoPrintForm, self).__init__(*args, **kwargs)
        self.fields['weight'].widget.attrs\
            .update({
                'class': 'form-control',
                'placeholder': 'total weight printed',
            })
        self.fields['unit'].widget.attrs\
            .update({
                'class': 'form-control',
                'placeholder': 'units printed',
            })
    
    def clean(self):
        super().clean()
        data = self.cleaned_data
        if data['weight'] > self.roll.weight:
            raise forms.ValidationError('Printing weight cannot excced Roll weight')
        if data['unit'] > self.roll.unit:
            raise forms.ValidationError('Printing Unit cannot excced Roll unit')
    
    def save(self):
        obj = super().save(commit = False)

        obj.color = self.roll.color
        obj.gsm = self.roll.gsm
        obj.print_type = 'Flexo'
        obj.width = self.roll.width
        obj.length = self.roll.length

        roll = self.roll
        roll.weight = round((roll.weight - obj.weight),2)
        roll.unit = roll.unit - obj.unit

        obj.save()
        roll.save()

        return obj

class OffsetPrintForm(ModelForm):
    class Meta:
        model = Bag
        exclude = ('roll', 'bag_type', 'status', 'print_type', 'height', 'width', 'create_timestamp', 'updated_timestamp')
    
    def __init__(self, *args, **kwargs):
        self.bag = kwargs.pop('bag', None)
        super(OffsetPrintForm, self).__init__(*args, **kwargs)
        self.fields['weight'].widget.attrs\
            .update({
                'class': 'form-control',
                'placeholder': 'total weight printed',
            })
    
    def clean(self):
        super().clean()
        data = self.cleaned_data
        if data['weight'] > self.bag.weight:
            raise forms.ValidationError('Printing weight cannot excced Bag weight')
    
    def save(self):
        obj = super().save(commit = False)

        obj.roll = self.bag.roll
        obj.bag_type = self.bag.bag_type
        obj.width = self.bag.width
        obj.height = self.bag.height
        obj.status = self.bag.status
        obj.print_type = 'Offset'

        bag = self.bag
        bag.weight = round((bag.weight - obj.weight),2)
        
        obj.save()
        bag.save()

        return obj



