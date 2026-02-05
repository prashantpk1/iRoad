from django.shortcuts import get_object_or_404, render,redirect
from core.core_forms import *
from django.views import View
from django.contrib import messages
from django.http import JsonResponse
# Create your views here.
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required

class EntityNatureCreateView(View):
    """View for creating Entity Nature"""
    
    def get(self, request,pk=None):
        if pk:
            # Fetch the existing record
            entity = get_object_or_404(EntityNature, pk=pk)
            # Initialize the form WITH the instance data
            form = EntityNatureForm(instance=entity)
        else:
            # Initialize an empty form for creation
            form = EntityNatureForm()
            
        return render(request, 'core/Account/entity_nature_form.html', {
            'form': form,
            'edit_id': pk # Useful for the template to know if it's an edit
        })
    
    def post(self, request,pk=None):
        if pk:
            entity = get_object_or_404(EntityNature, pk=pk)
            form = EntityNatureForm(request.POST, instance=entity)
        else:
            form = EntityNatureForm(request.POST)
        if form.is_valid():
            entity_nature = form.save()
            messages.success(request, f'Entity Nature "{entity_nature.entity_nature_code}" created successfully!')
            return redirect('entity_nature_list')
        else:
            messages.error(request, 'Please correct the errors below.')
        return render(request, 'core/Account/entity_nature_form.html', {'form': form, 'edit_id': pk})

class EntityNatureListView(View):
    """View for listing Entity Natures"""
    
    def get(self, request):
        entity_natures = EntityNature.objects.all().order_by('-id')
        context = {
            'entity_natures': entity_natures,
        }
        return render(request, 'core/Account/entity_nature_list.html', context)

class EntityAccountView(View):
    """
    Handles:
    - GET  : List + Create form + Edit form
    - POST : Create or Update Entity Account
    """

    def get(self, request, pk=None):
        entity_accounts = EntityAccount.objects.all().order_by('-id')
        if pk:
            entity = get_object_or_404(EntityAccount, pk=pk)
            form = EntityAccountForm(instance=entity)
            return render(request, 'core/Account/entity_account_form.html', {
                'form': form,
                'edit_id': pk
            })
        

    

        context = {
            'entity_accounts': entity_accounts,
            
        }
        return render(request, 'core/Account/entity_account_list.html', context)

  
class EntityAccountCreate(View):
    def get(self, request, pk=None):
        if pk:
            # Fetch the existing record
            entity = get_object_or_404(EntityAccount, pk=pk)
            # Initialize the form WITH the instance data
            form = EntityAccountForm(instance=entity)
        else:
            # Initialize an empty form for creation
            form = EntityAccountForm()
            
        return render(request, 'core/Account/entity_account_form.html', {
            'form': form,
            'edit_id': pk # Useful for the template to know if it's an edit
        })
    
    def post(self, request, pk=None):
        print("pk",pk)
        if pk:
            entity = get_object_or_404(EntityAccount, pk=pk)
            form = EntityAccountForm(request.POST, instance=entity)
            success_message = "Entity Account updated successfully!"
        else:
            form = EntityAccountForm(request.POST)
            success_message = "Entity Account created successfully!"

        if form.is_valid():
            form.save()
            messages.success(request, success_message)
            return redirect('entity_account_list')

      
        return render(request, 'core/Account/entity_account_form.html', {
            'form': form,
            'edit_id': pk
        })

class DocumentTypeCreateView(View):
    def get(self, request):
        form = DocumentTypeForm()
        return render(request, 'core/Account/document_type.html', {'form': form})
    
    def post(self, request):
        form=DocumentTypeForm(request.POST)
        if form.is_valid():
            document_type = form.save()
            messages.success(request, f'Document Type "{document_type.name_en}" created successfully!')
            return redirect('document_list')
        else:
            messages.error(request, 'Please correct the errors below.')
        return render(request, 'core/Account/document_type.html', {'form': form})
class DocumentCreateEditView(View):
    def get(self, request,pk=None):
        if pk:
            # Fetch the existing record
            entity = get_object_or_404(DocumentMaster, pk=pk)
            # Initialize the form WITH the instance data
            form = DocumentForm(instance=entity)
        else:
            # Initialize an empty form for creation
            form = DocumentForm()
            
        return render(request, 'core/Account/document_form.html', {
            'form': form,
            'edit_id': pk # Useful for the template to know if it's an edit
        })
       
    
    def post(self, request,pk=None):
        if pk:
            entity = get_object_or_404(DocumentMaster, pk=pk)
            form = DocumentForm(request.POST, request.FILES, instance=entity)
          
        else:
            form = DocumentForm(request.POST,request.FILES)
          
       
        if form.is_valid():
            document = form.save()
            messages.success(request, f'Document "{document.document_title}" created successfully!')
            return redirect('document_list')
        else:
            messages.error(request, 'Please correct the errors below.')
        return render(request, 'core/Account/document_form.html', {'form': form})
    
class DocumentListview(View):
    def get(self, request):
        documents = DocumentMaster.objects.all().order_by('-id')
        context = {
            'documents': documents,
        }
        return render(request, 'core/Account/document_list.html', context)


class SubAccountCreateView(View):
    def get(self, request,pk=None):
        if pk:
            # Fetch the existing record
            entity = get_object_or_404(SubAccount, pk=pk)
            # Initialize the form WITH the instance data
            form = SubAccountForm(instance=entity)
        else:
            # Initialize an empty form for creation
            form = SubAccountForm()
            
        return render(request, 'core/Account/sub_account_form.html', {
            'form': form,
            'edit_id': pk # Useful for the template to know if it's an edit
        })
       


     
    def post(self, request,pk=None):
        form = SubAccountForm(request.POST)


        if pk:
            entity = get_object_or_404(SubAccount, pk=pk)
            form = SubAccountForm(request.POST, instance=entity)
          
        else:
            form = SubAccountForm(request.POST)
          
       
        if form.is_valid():
            sub_account = form.save()
            messages.success(request, f'Sub Account "{sub_account.type_code}" created successfully!')
            return redirect('sub_account_list')
             
        else:
            messages.error(request, 'Please correct the errors below.')
        return render(request, 'core/Account/sub_account_form.html', {'form': form})
    
class SubAccountListView(View):
    def get(self, request):
        sub_accounts = SubAccount.objects.all().order_by('-id')
        context = {
            'sub_accounts': sub_accounts,
        }
        return render(request, 'core/Account/sub_account_list.html', context)
    



@login_required
def duplicate_entity_account(request, pk):
    entity = get_object_or_404(EntityAccount, pk=pk)
    entity.pk = None
    entity.display_name = f"{entity.display_name} (Copy)"
    entity.save()
    return redirect('entity_account_list')

@login_required
def entity_account_drawer(request, pk):
    """
    Single view that returns the drawer HTML content.
    This is called via AJAX when clicking a row.
    """
    entity = get_object_or_404(
        EntityAccount.objects.select_related('entity_nature'), 
        pk=pk
    )
    comments = entity.comments.filter(parent=None).select_related('user')
    
    return render(request, 'core/Account/entity_account_drawer.html', {
        'entity': entity,
        'comments': comments,
    })


@require_POST
@login_required
def add_entity_comment(request, pk):
    """
    Handle adding comments and replies.
    Returns JSON for AJAX requests, redirects for normal requests.
    """
    entity = get_object_or_404(EntityAccount, pk=pk)
    comment_text = request.POST.get('comment', '').strip()
    parent_id = request.POST.get('parent_id')
    
    if not comment_text:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'error': 'Comment cannot be empty'}, status=400)
        messages.error(request, 'Comment cannot be empty')
        return redirect('entity_account_list')
    
    parent = None
    if parent_id:
        try:
            parent = EntityAccountComment.objects.get(id=parent_id, entity_account=entity)
        except EntityAccountComment.DoesNotExist:
            pass
    
    comment = EntityAccountComment.objects.create(
        entity_account=entity,
        user=request.user,
        comment=comment_text,
        parent=parent
    )
    
    # If AJAX request, return the new comment HTML
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return render(request, 'core/Account/_comment_item.html', {
            'comment': comment,
            'is_reply': parent is not None,
        })
    
    messages.success(request, 'Comment added successfully')
    return redirect('entity_account_list')