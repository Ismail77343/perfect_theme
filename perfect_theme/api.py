import frappe

@frappe.whitelist(allow_guest=True)
def get_items():
    items = frappe.get_all('Item', fields=['name', 'item_name', 'description'])
    return items

@frappe.whitelist(allow_guest=True)
def render_page():
    items = get_items()
    context = {'items': items}
    return frappe.render_template('perfect_theme/web_template/cards_product/cards_product.html', context)-