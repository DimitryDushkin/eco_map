# coding: utf-8
from django import forms




class AddPointForm(forms.Form):
    name = forms.CharField(label='Название', max_length=255, required=False)
    adress = forms.CharField(label='Адрес',
                             max_length=512,
                             widget=forms.widgets.TextInput(attrs={'class':'input-xlarge'}))
    
    WASTE_TYPES = (("Paper", "Бумага"),
               ("Glass", "Стекло"),
               ("Metall", "Метал"),
               ("Plastic", "Пластик"),
               ("Danger", "Опасные отходы"),
               ("Cloth", "Одежда"),
               ("Other", "Прочее")
              )
    
    waste_types = forms.MultipleChoiceField(
                    widget=forms.widgets.CheckboxSelectMultiple(attrs={'class':'input-xlarge'}),
                    choices=WASTE_TYPES)
    work_time = forms.CharField(label='Время работы',
                                max_length=255,
                                widget=forms.widgets.TextInput(attrs={'class':'input-xlarge'}), 
                                required=False)
    phone = forms.CharField(label='Телефон', 
                            max_length=255,
                            widget=forms.widgets.TextInput(attrs={'class':'input-xlarge'}), 
                            required=False)
    comment = forms.CharField(label='Примечения',
                              widget=forms.widgets.Textarea(),
                              required=False)
    