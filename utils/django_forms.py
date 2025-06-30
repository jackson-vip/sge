# Função para adicionar um atributo a um campo de formulário
from django import forms


def add_attr(field, attr_name, attr_new_value):
    existing = field.widget.attrs.get(attr_name, '')
    field.widget.attrs[attr_name] = f'{existing} {attr_new_value}'.strip()

# Função para adicionar um placeholder a um campo de formulário
def add_placeholder(field, placeholder_val):
    add_attr(field, 'placeholder', placeholder_val) 

# Função para renomear um label de um campo de formulário
def rename_label(field, new_label):
    field.label = new_label

# Função para adicionar um texto de ajuda a um campo de formulário
def add_help_text(field, help_text):
    field.help_text = help_text

def add_form_control(self):
    for field_name, field in self.fields.items():
        if field and isinstance(field, forms.ModelChoiceField):
            field.widget.attrs['class'] = 'selectpicker'
            field.widget.attrs['data-live-search'] = 'true'
            field.widget.attrs['data-dropup-auto'] = 'false'
        if field and isinstance(field, forms.Select):
            field.widget.attrs['class'] = 'selectpicker'
            field.widget.attrs['data-live-search'] = 'true'
            field.widget.attrs['data-dropup-auto'] = 'false'
        if field and isinstance(field, forms.ChoiceField):
            field.widget.attrs['class'] = 'selectpicker'
            field.widget.attrs['data-live-search'] = 'true'
            field.widget.attrs['data-dropup-auto'] = 'false'
        elif field and isinstance(field, forms.TypedChoiceField):
            field.widget.attrs['class'] = 'selectpicker'
            field.widget.attrs['data-live-search'] = 'true'
            field.widget.attrs['data-dropup-auto'] = 'false'
        elif field and isinstance(field, forms.ModelMultipleChoiceField):
            field.widget.attrs['class'] = 'selectpicker'
            field.widget.attrs['data-live-search'] = 'true'
            field.widget.attrs['data-actions-box'] = 'true'
            field.widget.attrs['data-dropup-auto'] = 'false'
        elif field and isinstance(field, forms.MultipleChoiceField):
            field.widget.attrs['class'] = 'selectpicker'
            field.widget.attrs['data-live-search'] = 'true'
            field.widget.attrs['data-actions-box'] = 'true'
            field.widget.attrs['data-dropup-auto'] = 'false'
        elif field and isinstance(field, forms.SelectMultiple):
            field.widget.attrs['class'] = 'selectpicker '
            field.widget.attrs['data-live-search'] = 'true'
            field.widget.attrs['data-actions-box'] = 'true'
            field.widget.attrs['data-dropup-auto'] = 'false'
        elif field and isinstance(field, forms.DateField):
            field.widget.attrs['class'] = 'date datepicker'
            field.widget.attrs['autocomplete'] = 'off'
        else:
            field.widget.attrs['class'] = 'form-control'