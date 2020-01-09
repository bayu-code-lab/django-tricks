#region widgets.py
from django import forms

class CustomSelect(forms.widgets.Select):
    def __init__(self, attrs=None, choices=(), modify_choices=()):
        super(CustomSelect, self).__init__(attrs, choices=choices)
        # set data
        self.modify_choices = modify_choices

    def create_option(self, name, value, label, selected, index, subindex=None, attrs=None):
        option = super(CustomSelect, self).create_option(name, value, label, selected, index, subindex, attrs)
        for a, b, c, d in self.modify_choices:
            #your statement
            if value == a:
                option['attrs']['color-code'] = b
                option['attrs']['hex-code'] = c
                option['attrs']['hex-code-style'] = d
        return option
#endregion

#region forms.py
from . import models
from . import widgets as customWidget

class MyForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(MyForm, self).__init__(*args, **kwargs)
        get_car_variant_color_data = models.MyColorModels.objects.filter(variant=self.instance.color.id, is_deleted=False)
        self.fields['color'] = forms.ModelChoiceField(
            initial=None, queryset=get_car_variant_color_data, 
            widget=customWidget.CustomSelect(modify_choices=tuple(get_car_variant_color_data.values_list('id','code', 'color_alias__hex_code', 'color_alias__hex_code_style'))))
#endregion