from django.shortcuts import get_object_or_404, render,redirect
from core.core_forms import *
from django.views import View
from django.contrib import messages
# Create your views here.


class EntityNatureCreateView(View):
    """View for creating Entity Nature"""
    
    def get(self, request):
        form = EntityNatureForm()
        return render(request, 'core/Account/entity_nature_form.html', {'form': form})
    
    def post(self, request):
        form = EntityNatureForm(request.POST)
        if form.is_valid():
            entity_nature = form.save()
            messages.success(request, f'Entity Nature "{entity_nature.entity_nature_code}" created successfully!')
            return render(request, 'core/success.html', {
                'message': f'Entity Nature "{entity_nature.entity_nature_code}" has been created successfully!'
            })
        else:
            messages.error(request, 'Please correct the errors below.')
        return render(request, 'core/Account/entity_nature_form.html', {'form': form})


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
            return render(request, 'core/success.html', {
                'message': f'Document Type "{document_type.name_en}" has been created successfully!'
            })
        else:
            messages.error(request, 'Please correct the errors below.')
        return render(request, 'core/Account/document_type.html', {'form': form})
class DocumentView(View):
    def get(self, request):
        form = DocumentForm()
        return render(request, 'core/Account/document.html',{'form': form})
    
    def post(self, request):
        form=DocumentForm(request.POST,request.FILES)
        if form.is_valid():
            document = form.save()
            messages.success(request, f'Document "{document.document_title}" created successfully!')
            return render(request, 'core/success.html', {
                'message': f'Document "{document.document_title}" has been created successfully!'
            })
        else:
            messages.error(request, 'Please correct the errors below.')
        return render(request, 'core/Account/document.html', {'form': form})
    

class SubAccountCreateView(View):
    def get(self, request):
        form = SubAccountForm()
        return render(request, 'core/Account/sub_account_form.html', {'form': form})
    
    def post(self, request):
        form = SubAccountForm(request.POST)
        if form.is_valid():
            sub_account = form.save()
            messages.success(request, f'Sub Account "{sub_account.type_code}" created successfully!')
            return render(request, 'core/success.html', {
                'message': f'Sub Account "{sub_account.type_code}" has been created successfully!'
            })
        else:
            messages.error(request, 'Please correct the errors below.')
        return render(request, 'core/Account/sub_account_form.html', {'form': form})