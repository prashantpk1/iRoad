from django.urls import path
from core.views import *
urlpatterns = [
    # path('entity-natures/create/', EntityNatureCreateView.as_view(), name='entity_nature_create'),
    # path('entity-natures/<int:pk>/', EntityNatureCreateView.as_view(), name='entity_nature_edit'),
    
    # path('entity-accounts/', EntityAccountView.as_view(), name='entity_account_list'),
    # path('entity-accounts/create/', EntityAccountCreate.as_view(), name='entity_account_create'),
    # path('entity-accounts/<int:pk>/', EntityAccountCreate.as_view(), name='entity_account_edit'),  

    # path('entity-natures/', EntityNatureListView.as_view(), name='entity_nature_list'), 

    # path('document/', DocumentCreateEditView.as_view(), name='document_create'),
    # path('document/<int:pk>/', DocumentCreateEditView.as_view(), name='document_edit'),
    # path('document-list/', DocumentListview.as_view(), name='document_list'),
    # path('document-type/', DocumentTypeCreateView.as_view(), name='document_type_create'),
    # path('sub-account/', SubAccountCreateView.as_view(), name='sub_account_create'),
    # path('sub-account/<int:pk>/', SubAccountCreateView.as_view(), name='sub_account_edit'),
    # path('sub-account-list/', SubAccountListView.as_view(), name='sub_account_list'),

    # path('entity/<int:pk>/', entity_account_detail, name='entity_account_detail'),
    # path('entity/<int:pk>/comment/', add_entity_comment, name='entity_account_comment'),
    # path('entity/<int:pk>/duplicate/', duplicate_entity_account, name='entity_account_duplicate'),
    # path('entity/<int:pk>/detail/', entity_account_detail_partial, name='entity_account_detail_partial'),
    # path('entity/<int:pk>/drawer/',entity_account_detail_drawer,name='entity_account_detail_drawer'),

    # path('entity-account/<int:pk>/detail-api/', entity_account_detail_api, name='entity_account_detail_api'),
    path('entity-natures/', EntityNatureListView.as_view(), name='entity_nature_list'), 
    path('entity-natures/create/', EntityNatureCreateView.as_view(), name='entity_nature_create'),
    path('entity-natures/<int:pk>/edit/', EntityNatureCreateView.as_view(), name='entity_nature_edit'),  # add /edit/
    
    # Entity Account
    path('entity-accounts/', EntityAccountView.as_view(), name='entity_account_list'),
    path('entity-accounts/create/', EntityAccountCreate.as_view(), name='entity_account_create'),
    path('entity-accounts/<int:pk>/edit/', EntityAccountCreate.as_view(), name='entity_account_edit'),  # add /edit/
    
    # Document
    path('documents/', DocumentListview.as_view(), name='document_list'),  # plural
    path('documents/create/', DocumentCreateEditView.as_view(), name='document_create'),
    path('documents/<int:pk>/edit/', DocumentCreateEditView.as_view(), name='document_edit'),  # add /edit/
    path('document-types/create/', DocumentTypeCreateView.as_view(), name='document_type_create'),  # plural and /create/
    
    # Sub Account
    path('sub-accounts/', SubAccountListView.as_view(), name='sub_account_list'),  # plural
    path('sub-accounts/create/', SubAccountCreateView.as_view(), name='sub_account_create'),  # add /create/
    path('sub-accounts/<int:pk>/edit/', SubAccountCreateView.as_view(), name='sub_account_edit'),  # add /edit/

    # Drawer & Actions
    path('entity-accounts/<int:pk>/drawer/', entity_account_drawer, name='entity_account_drawer'),
    path('entity-accounts/<int:pk>/comment/', add_entity_comment, name='entity_account_comment'),
    path('entity-accounts/<int:pk>/duplicate/', duplicate_entity_account, name='entity_account_duplicate'),


    # path('entity-natures/<int:pk>/detail/', entity_nature_detail_api, name='entity_nature_detail_api'),
    # path('entity-natures/<int:pk>/comment/', add_entity_nature_comment, name='entity_nature_comment'),
    # path('entity-natures/<int:pk>/duplicate/', duplicate_entity_nature, name='entity_nature_duplicate'),
    # path('entity-natures/<int:pk>/delete/', delete_entity_nature, name='entity_nature_delete'),
    # path('entity-natures/<int:pk>/toggle-status/', toggle_entity_nature_status, name='entity_nature_toggle_status'),    

]
