from django import forms
from django.core.exceptions import ValidationError
from core.models import *



class EntityNatureForm(forms.ModelForm):
    class Meta:
        model = EntityNature
        fields = [
            'entity_nature_code',
            'entity_nature_type',
            'entity_nature_status',
            'entity_nature_nationality',
            'entity_nature_label_arabic',
            'entity_nature_residency',
            'entity_nature_label_english'
        ]
        widgets = {
            'entity_nature_code': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Enter unique entity nature code'
            }),
            'entity_nature_type': forms.Select(attrs={
                'class': 'form-select'
            }),
            'entity_nature_status': forms.Select(attrs={
                'class': 'form-select'
            }),
            'entity_nature_nationality': forms.Select(attrs={
                'class': 'form-select'
            }),
            'entity_nature_label_arabic': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'أدخل التسمية بالعربية',
                'dir': 'rtl'
            }),
            'entity_nature_residency': forms.Select(attrs={
                'class': 'form-select'
            }),
            'entity_nature_label_english': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Enter label in English'
            }),
        }


class EntityAccountForm(forms.ModelForm):
    class Meta:
        model = EntityAccount
        fields = [
            'entity_id',
            'english_name',
            'entity_nature',
            'display_name',
            'entity_type',
            'account_status',
            'arabic_name',
            'verification_status',
            'primary_identifier_number',
            'primary_identifier_issue_date',
            'primary_identifier_expiry_date',
            'vat_registration_status'
        ]
        widgets = {
            'entity_id': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Enter unique entity ID'
            }),
            'english_name': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Enter entity name in English'
            }),
            'entity_nature': forms.Select(attrs={
                'class': 'form-select'
            }),
            'display_name': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Enter display name'
            }),
            'entity_type': forms.Select(attrs={
                'class': 'form-select'
            }),
            'account_status': forms.Select(attrs={
                'class': 'form-select'
            }),
            'arabic_name': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'أدخل اسم الكيان بالعربية',
                'dir': 'rtl'
            }),
            'verification_status': forms.Select(attrs={
                'class': 'form-select'
            }),
            'primary_identifier_number': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Enter Commercial Registration Number'
            }),
            'primary_identifier_issue_date': forms.DateInput(attrs={
                'class': 'form-input',
                'type': 'date'
            }),
            'primary_identifier_expiry_date': forms.DateInput(attrs={
                'class': 'form-input',
                'type': 'date'
            }),
            'vat_registration_status': forms.Select(attrs={
                'class': 'form-select'
            }),
        }


class DocumentTypeForm(forms.ModelForm):
    class Meta:
        model = DocumentType
        fields = "__all__"

class DocumentForm(forms.ModelForm):
    class Meta:
        model = DocumentMaster
        fields = [
            'document_id', 'document_type', 'document_title', 
            'document_number', 'document_certificate_ref_no', 
            'entity_account', 'issue_date', 'registration_date', 
            'is_expiry_applicable', 'expiry_date', 'validity_status', 
            'document_status', 'attachment_file'
        ]
        
        # Adding the DateInput widget for date fields
        widgets = {
            'issue_date': forms.DateInput(attrs={'type': 'date'}),
            'registration_date': forms.DateInput(attrs={'type': 'date'}),
            'expiry_date': forms.DateInput(attrs={'type': 'date'}),
        }
    


class SubAccountForm(forms.ModelForm):
    class Meta:
        model = SubAccount
        fields = "__all__"