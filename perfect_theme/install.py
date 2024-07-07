# # apps/perfect_theme/perfect_theme/install.py
# import frappe

# def after_install():
#     custom_header_include = '<header>{% include "perfect_theme/templates/includes/perfect_theme_header.html" %}</header>'
    
#     website_settings = frappe.get_doc('Website Settings')
#     if not any(custom_header_include in item.item_label for item in website_settings.top_bar_items):
#         website_settings.append('top_bar_items', {
#             'item_label': custom_header_include,
#             'item_type': 'HTML',
#             'item_route': '',
#             'is_standard': 1
#         })
#         website_settings.save()

# def before_uninstall():
#     custom_header_include = '<header>{% include "perfect_theme/templates/includes/perfect_theme_header.html" %}</header>'
    
#     website_settings = frappe.get_doc('Website Settings')
#     website_settings.top_bar_items = [
#         item for item in website_settings.top_bar_items
#         if custom_header_include not in item.item_label
#     ]
#     website_settings.save()
