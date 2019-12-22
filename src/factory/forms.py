from django.forms import ModelForm
from django.forms import forms
from .models import Roll, Bag, Ship

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
        self.fields['roll_type'].widget.attrs\
            .update({
                'class': 'form-control'
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
                'placeholder': 'Width',
            })
        self.fields['weight'].widget.attrs\
            .update({
                'class': 'form-control',
                'placeholder': 'Weight',
            })
        self.fields['unit'].widget.attrs\
            .update({
                'class': 'form-control',
                'placeholder': 'Unit',
            })
    

class BagForm(ModelForm):
    class Meta:
        model = Bag
        exclude = ('status', 'create_timestamp', 'updated_timestamp')
    
    def __init__(self, *args, **kwargs):
        super(BagForm, self).__init__(*args, **kwargs)
        self.fields['roll'].widget.attrs\
            .update({
                'class': 'form-control'
            })
        self.fields['unit'].widget.attrs\
            .update({
                'class': 'form-control',
                'placeholder': 'Unit',
            })
        self.fields['weight'].widget.attrs\
            .update({
                'class': 'form-control',
                'placeholder': 'Weight',
            })
        if self.instance:
            self.fields['roll'].queryset = Roll.objects.filter(unit__gt=0).order_by('color', 'gsm', 'width', 'weight', 'unit')

    def clean(self):
        super().clean()
        data = self.cleaned_data
        bag_unit = data['unit']
        roll_unit = data['roll'].unit

        bag_weight = data['weight']
        roll_weight = data['roll'].weight

        bag_unit = data['unit']
        roll_unit = data['roll'].unit

        if bag_unit > roll_unit:
            raise forms.ValidationError('Bag unit can not be greater than Roll Unit')
            
        if bag_weight > roll_weight:
            raise forms.ValidationError('Bag weight can not be greater than Roll Weight')

        if (bag_weight/bag_unit) > (roll_weight/roll_unit):
            raise forms.ValidationError('Bag weight/unit can not be greater than Roll Weight/Unit')

class ShipForm(ModelForm):
    class Meta:
        model = Ship
        exclude = ('assingment_timestamp', 'assigned_by')


    def __init__(self, *args, **kwargs):
        super(ShipForm, self).__init__(*args, **kwargs)
        self.fields['bag'].widget.attrs\
            .update({
                'class': 'form-control'
            })
        self.fields['distributor'].widget.attrs\
            .update({
                'class': 'form-control'
            })
        if self.instance:
            self.fields['bag'].queryset = Bag.objects.filter(status='STOCKED')
    
    def save(self, user):
        obj = super().save(commit = False)
        obj.assigned_by = user
        obj.save()
        return obj