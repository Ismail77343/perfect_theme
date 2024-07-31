import frappe
import requests


@frappe.whitelist()
def install():
    url = 'https://raw.githubusercontent.com/Ismail77343/perfect_theme/main/_install.txt'
    
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        frappe.throw(f'فشل في تحميل الملف، الحالة: {response.status_code}')


@frappe.whitelist(allow_guest=True)
def get_items():
    items = frappe.get_all('Item', fields=['name', 'item_name', 'description'])
    return items



@frappe.whitelist(allow_guest=True)
def render_page():
    items = get_items()
    context = {'items': items}
    return frappe.render_template('perfect_theme/web_template/cards_product/cards_product.html', context)