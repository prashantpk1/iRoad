from django.db import models
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from App.models import User


# Create your models here.

class EntityNature(models.Model):
    """
    Model for Entity Nature with detailed attributes
    """
    
    # Entity Nature Type Choices
    ENTITY_NATURE_TYPE_CHOICES = [
        ('individual', 'Individual'),
        ('corporate', 'Corporate'),
        ('government', 'Government'),
        ('non_profit', 'Non-Profit'),
    ]
    
    # Entity Nature Status Choices
    ENTITY_NATURE_STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ]
    
    # Nationality Choices
    NATIONALITY_CHOICES = [
        ('saudi', 'Saudi'),
        ('gcc', 'GCC'),
        ('foreign', 'Foreign'),
    ]
    
    # Residency Choices
    RESIDENCY_CHOICES = [
        ('resident', 'Resident'),
        ('non_resident', 'Non-Resident'),
    ]
    
    entity_nature_code = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="Entity Nature Code",
      
    )
    
    entity_nature_type = models.CharField(
        max_length=50,
        choices=ENTITY_NATURE_TYPE_CHOICES,
        verbose_name="Entity Nature Type"
    )
    
    entity_nature_status = models.CharField(
        max_length=50,
        choices=ENTITY_NATURE_STATUS_CHOICES,
        default='active',
        verbose_name="Entity Nature Status"
    )
    
    entity_nature_nationality = models.CharField(
        max_length=50,
        choices=NATIONALITY_CHOICES,
        verbose_name="Entity Nature Nationality"
    )
    
    entity_nature_label_arabic = models.CharField(
        max_length=255,
        verbose_name="Entity Nature Label (Arabic)",
        
    )
    
    entity_nature_residency = models.CharField(
        max_length=50,
        choices=RESIDENCY_CHOICES,
        verbose_name="Entity Nature Residency"
    )
    
    entity_nature_label_english = models.CharField(
        max_length=255,
        verbose_name="Entity Nature Label (English)",
       
    )
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.entity_nature_code
    

class EntityAccount(models.Model):
    """
    Model for creating and managing entity accounts with account information,
    CR (Commercial Registration) details, and VAT information.
    """
    
    # Entity Nature Choices
    
    
    # Entity Type Choices
    ENTITY_TYPE_CHOICES = [
        ('llc', 'Limited Liability Company'),
        ('sole_proprietorship', 'Sole Proprietorship'),
        ('public_company', 'Public Company'),
        ('private_company', 'Private Company'),
    ]
    
    # Account Status Choices
    ACCOUNT_STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('pending', 'Pending'),
        ('suspended', 'Suspended'),
    ]
    
    # Verification Status Choices
    VERIFICATION_STATUS_CHOICES = [
        ('verified', 'Verified'),
        ('unverified', 'Unverified'),
        ('pending', 'Pending Verification'),
        ('rejected', 'Rejected'),
    ]
    
    # VAT Registration Status Choices
    VAT_STATUS_CHOICES = [
        ('registered', 'Registered'),
        ('unregistered', 'Unregistered'),
        ('pending', 'Pending Registration'),
        ('exempt', 'Exempt'),
    ]
    
    # ==================== Account Information ====================
    entity_id = models.CharField(
        max_length=50,
        verbose_name="Entity ID",
        
    )
    
    english_name = models.CharField(
        max_length=255,
        verbose_name="English Name",
        
    )
    
    entity_nature = models.ForeignKey(
        EntityNature,
        on_delete=models.PROTECT,
        related_name='entity_accounts',
        verbose_name="Entity Nature",
      
    )
    
    display_name = models.CharField(
        max_length=255,
        verbose_name="Display Name",
       
    )
    
    entity_type = models.CharField(
        max_length=50,
        choices=ENTITY_TYPE_CHOICES,
        verbose_name="Entity Type"
    )
    
    account_status = models.CharField(
        max_length=50,
        choices=ACCOUNT_STATUS_CHOICES,
        default='pending',
        verbose_name="Account Status"
    )
    
    arabic_name = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Arabic Name",
        
    )
    
    verification_status = models.CharField(
        max_length=50,
        choices=VERIFICATION_STATUS_CHOICES,
        default='unverified',
        verbose_name="Verification Status"
    )
    
    # ==================== CR Information ====================
    primary_identifier_number = models.CharField(
        max_length=100,
        verbose_name="Primary Identifier Number",
        
    )
    
    primary_identifier_issue_date = models.DateField(
        verbose_name="Primary Identifier Issue Date",
       
    )
    
    primary_identifier_expiry_date = models.DateField(
        verbose_name="Primary Identifier Expiry Date",
        
    )
    
    # ==================== VAT Information ====================
    vat_registration_status = models.CharField(
        max_length=50,
        choices=VAT_STATUS_CHOICES,
        verbose_name="VAT Registration Status"
    )
    
    vat_number = models.CharField(
        max_length=15,
        blank=True,
        null=True,
        validators=[
            RegexValidator(
                regex=r'^\d{15}$',
                message='VAT Number must be 15 digits'
            )
        ],
        verbose_name="VAT Number",
      
    )
    
    vat_registration_date = models.DateField(
        blank=True,
        null=True,
        verbose_name="VAT Registration Date",
       
    )
    
    # ==================== Metadata ====================
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.english_name
    



class EntityAccountComment(models.Model):
    entity_account = models.ForeignKey(
        EntityAccount,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    parent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='replies'
    )
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']



class DocumentType(models.Model):
    name_en = models.CharField(
        max_length=100,
        unique=True
    )
    name_ar = models.CharField(
        max_length=100,
        unique=True
    )
    def __str__(self):
        return self.name_en

class DocumentMaster(models.Model):

    # -------------------------
    # BASIC DOCUMENT DETAILS
    # -------------------------
    document_id = models.CharField(
        max_length=50,
        unique=True
    )

    document_type = models.ForeignKey(
        'DocumentType',
        on_delete=models.PROTECT,
        related_name='documents'
    )

    document_title = models.CharField(
        max_length=255
    )

    document_number = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    document_certificate_ref_no = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    # -------------------------
    # ENTITY DETAILS
    # -------------------------
    entity_account = models.ForeignKey(
        'EntityAccount',
        on_delete=models.PROTECT,
        related_name='documents'
    )

    # -------------------------
    # DATE FIELDS
    # -------------------------
    issue_date = models.DateField(blank=True, null=True)

    registration_date = models.DateField(
        blank=True,
        null=True
    )

    is_expiry_applicable = models.BooleanField(
        default=False
    )

    expiry_date = models.DateField(
        blank=True,
        null=True
    )

    # -------------------------
    # STATUS FIELDS
    # -------------------------
    VALIDITY_STATUS_CHOICES = [
        ('valid', 'Valid'),
        ('expired', 'Expired'),
        ('under_review', 'Under Review'),
    ]

    validity_status = models.CharField(
        max_length=20,
        choices=VALIDITY_STATUS_CHOICES,
        default='valid'
    )

    DOCUMENT_STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('pending', 'Pending'),
    ]

    document_status = models.CharField(
        max_length=20,
        choices=DOCUMENT_STATUS_CHOICES,
        default='active'
    )

    # -------------------------
    # FILE ATTACHMENT
    # -------------------------
    attachment_file = models.FileField(
        upload_to='documents/',
        blank=True,
        null=True
    )

    # -------------------------
    # AUDIT FIELDS
    # -------------------------
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f"{self.document_title} ({self.document_id})"
    



class SubAccount(models.Model):

    # -------------------------
    # BASIC DETAILS
    # -------------------------
    type_code = models.CharField(
        max_length=50,
        unique=True
    )

    arabic_label = models.CharField(
        max_length=255
    )

    english_label = models.CharField(
        max_length=255
    )

    # -------------------------
    # YES / NO DROPDOWNS
    # -------------------------
    YES_NO_CHOICES = [
        ('yes', 'Yes'),
        ('no', 'No'),
    ]

    is_enabled = models.CharField(
        max_length=3,
        choices=YES_NO_CHOICES,
        default='yes'
    )

    allow_provisional_mode = models.CharField(
        max_length=3,
        choices=YES_NO_CHOICES,
        default='no'
    )

    requires_credit_limit = models.CharField(
        max_length=3,
        choices=YES_NO_CHOICES,
        default='no'
    )

    requires_agreement = models.CharField(
        max_length=3,
        choices=YES_NO_CHOICES,
        default='no'
    )

    requires_admin_approval = models.CharField(
        max_length=3,
        choices=YES_NO_CHOICES,
        default='no'
    )

    # -------------------------
    # ACCOUNT PURPOSE (FIXED)
    # -------------------------
    ACCOUNT_PURPOSE_CHOICES = [
        ('sales', 'Sales'),
        ('purchases', 'Purchases'),
        ('both', 'Both'),
    ]

    account_purpose = models.CharField(
        max_length=10,
        choices=ACCOUNT_PURPOSE_CHOICES
    )

    # -------------------------
    # AUDIT FIELDS
    # -------------------------
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.english_label} ({self.type_code})"



class EntityNatureComment(models.Model):
    entity_nature = models.ForeignKey(EntityNature, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Comment by {self.user} on {self.entity_nature}"