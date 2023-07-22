from django import forms
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from .models import *
import re


class ClienteForm(forms.Form):

    name = forms.CharField(
        max_length=100, 
        label="Nome",
        widget=forms.TextInput(
            attrs={'placeholder': 'Nome'}))
    
    cpf = forms.CharField(
        max_length=14,  
        label="CPF",
        widget=forms.TextInput(
            attrs={'placeholder': '000.000.000-00'}))
    
    phone = forms.CharField(
        max_length=15, 
        label="Telefone",
        widget=forms.TextInput(
            attrs={'placeholder': '(00) 00000-0000'}))
    
    address = forms.CharField(
        max_length=150, 
        label="Endereço",
        widget=forms.TextInput(
            attrs={'placeholder': "Rua, N, Bairro, Cidade - Estado"}))
    

    def __init__(self, *args, **kwargs):
        self.instance = kwargs.pop('instance', None)
        super().__init__(*args, **kwargs)


    def clean_cpf(self):
        cpf = self.cleaned_data['cpf']
        cpf_without_mask = re.sub(r'[^\d]', '', cpf)

        if len(cpf_without_mask) != 11:
            raise forms.ValidationError('O CPF deve conter 11 dígitos.')
        
        if self.instance:
            if Client.objects.exclude(pk=self.instance.pk).filter(cpf=cpf).exists():
                raise forms.ValidationError('CPF já cadastrado. Verifique o número informado.')
        
        else:
            if Client.objects.filter(cpf=cpf).exists():
                raise forms.ValidationError('CPF já cadastrado. Verifique o número informado.')
        
        if not re.match(r'^\d{3}\.\d{3}\.\d{3}\-\d{2}$', cpf):
            raise forms.ValidationError('Tente um cpf válido. Ex. 000.000.000-00')

        if not self.validar_cpf(cpf_without_mask):
            raise forms.ValidationError('CPF inválido.')
        
        return cpf
    

    # codigo para calculo de cpf valido
    def validar_cpf(self, cpf):
        # Verifica se todos os dígitos são iguais, o que torna o CPF inválido
        if len(set(cpf)) == 1:
            return False

        # Cálculo do primeiro dígito verificador
        soma = sum(int(cpf[i]) * (10 - i) for i in range(9))
        resto = soma % 11
        digito1 = 0 if resto < 2 else 11 - resto

        # Verifica se o primeiro dígito verificador é válido
        if int(cpf[9]) != digito1:
            return False

        # Cálculo do segundo dígito verificador
        soma = sum(int(cpf[i]) * (11 - i) for i in range(10))
        resto = soma % 11
        digito2 = 0 if resto < 2 else 11 - resto

        # Verifica se o segundo dígito verificador é válido
        if int(cpf[10]) != digito2:
            return False

        return True
            


# Formulário de vendas

class SaleForm(forms.Form):

    products = forms.MultipleChoiceField(
        label='Produtos',
        widget=forms.Select(attrs={'class': 'select-multiple'}),
        error_messages={}
    )

    amount = forms.IntegerField(
        label='Quantidade',
        widget=forms.NumberInput(attrs={'value': '1', 'min': '1'}),
    )  

    def __init__(self, *args, **kwargs):
        super(SaleForm, self).__init__(*args, **kwargs)
        products_choices = self.get_available_products()
        self.fields['products'].choices = products_choices


    def get_available_products(self):
        available_products = Products.objects.filter(amount__gt=0)
        products_choices = [(product.id, product.name) for product in available_products]
        products_choices.insert(0, ('', '------'))

        return products_choices