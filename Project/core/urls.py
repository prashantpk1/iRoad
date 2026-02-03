from django.urls import path
from core.views import *
urlpatterns = [
    path('entity-nature/', EntityNatureCreateView.as_view(), name='entity_nature_create'),
    
    path('entity-accounts/', EntityAccountView.as_view(), name='entity_account_list'),
    path('entity-accounts/<int:pk>/', EntityAccountView.as_view(), name='entity_account_edit'),    

    path('document/', DocumentView.as_view(), name='document_create'),
    path('document-type/', DocumentTypeCreateView.as_view(), name='document_type_create'),
    path('sub-account/', SubAccountCreateView.as_view(), name='sub_account_create'),

]
