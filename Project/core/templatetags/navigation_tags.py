from django import template

register = template.Library()

@register.filter
def get_section(url_name):
    """
    Determine the main navigation section based on the current URL name
    """
    if not url_name:
        return 'Accounts'
    
    # Map URL names to sections
    section_mapping = {
        # Accounts section
        'entity_account_list': 'Accounts',
        'entity_account_create': 'Accounts',
        'entity_account_edit': 'Accounts',
        'entity_nature_list': 'Accounts',
        'entity_nature_create': 'Accounts',
        'entity_nature_edit': 'Accounts',
        'document_list': 'Accounts',
        'document_create': 'Accounts',
        'document_edit': 'Accounts',
        'sub_account_list': 'Accounts',
        'sub_account_create': 'Accounts',
        'sub_account_edit': 'Accounts',
        
        # Add other sections as needed
        # 'service_list': 'Services',
        # 'pricing_list': 'Pricing',
    }
    
    return section_mapping.get(url_name, 'Accounts')

@register.simple_tag(takes_context=True)
def get_current_section(context):
    """
    Get current section from request or context
    """
    request = context.get('request')
    if request:
        return get_section(request.resolver_match.url_name)
    return 'Accounts'