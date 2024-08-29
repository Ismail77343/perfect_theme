import frappe;
from frappe import _

def after_install():
    create_accounts()
    create_item_tax_templates()
    create_ksa_vat_settings()
    ExecuteSales()
    ExecuteBuy()
    
def create_accounts():
    create_account(" Excise 100% ")
    create_account(" Excise 50% ")
    create_account(" VAT 15% ")
    create_account(" VAT 5% ")
    create_account(" VAT Zero ")


def create_account(account_name):
        # جلب جميع الشركات في النظام
    companies = frappe.get_all("Company", fields=["name"])
    
    for company in companies:
        company_name = company['name']
        
        # البحث عن حساب رئيسي من نوع Tax ويكون is_group=1 لكل شركة
        parent_account = frappe.db.get_value("Account", {"account_type": "Tax", "is_group": 1, "company": company_name}, "name")
        
        if not parent_account:
            # إذا لم يتم العثور على حساب من نوع Tax ويكون is_group=1
            frappe.throw(f"No group account of type 'Tax' found in company {company_name}. Please create one first.")
        
        # تحقق إذا كان الحساب الذي تريد إضافته موجود لكل شركة
        if not frappe.db.exists("Account", {"account_name": account_name, "company": company_name}):
            # إذا لم يكن موجود، قم بإضافته تحت الحساب الرئيسي
            new_account = frappe.get_doc({
                "doctype": "Account",
                "account_name": account_name,
                "parent_account": parent_account,
                "company": company_name,
                "is_group": 0,  # حساب فرعي
                "root_type": frappe.db.get_value("Account", parent_account, "root_type"),
                "report_type": frappe.db.get_value("Account", parent_account, "report_type"),
                "account_type": "Tax"  # أو أي نوع آخر حسب الحاجة
            })
            new_account.insert(ignore_permissions=True)
            frappe.msgprint(f"Account '{account_name}' has been added under '{parent_account}' in company '{company_name}'.")
        else:
            frappe.msgprint(f"Account '{account_name}' already exists in company '{company_name}'.")


def create_item_tax_templates():
    companies = frappe.get_all("Company", fields=["name"])

    for company in companies:
        company_name = company['name']
        # Example usage
        tax_rates = [
            {'tax_type': ' Excise 100% ', 'rate': 100},
        ]
        create_item_tax_template(" Excise 100% ", tax_rates, company_name)
        
        tax_rates = [
            {'tax_type': ' Excise 50% ', 'rate': 50},
        ]
        create_item_tax_template(" Excise 50% ", tax_rates, company_name)

        tax_rates = [
            {'tax_type': ' VAT 15% ', 'rate': 15},
        ]
        create_item_tax_template(" VAT 15% ", tax_rates, company_name)

        tax_rates = [
            {'tax_type': ' VAT 5% ', 'rate': 5},
        ]
        create_item_tax_template(" VAT 5% ", tax_rates, company_name)

        tax_rates = [
            {'tax_type': ' VAT Zero ', 'rate': 0},
        ]
        create_item_tax_template(" VAT Zero ", tax_rates, company_name)

def create_item_tax_template(template_name, tax_rates, company_name):
    """
    Create an Item Tax Template and add tax accounts in the Tax Rates table.
    
    :param template_name: Name of the Item Tax Template.
    :param tax_rates: List of dictionaries with 'tax_type' and 'rate' keys.
    :param company_name: Name of the company for which the accounts are being created.
    Example: [{'tax_type': 'VAT 15%', 'rate': 15}, {'tax_type': 'VAT 5%', 'rate': 5}]
    """
    try:
        # Create a new Item Tax Template
        item_tax_template = frappe.get_doc({
            "doctype": "Item Tax Template",
            "title": template_name,
            "taxes": []
        })
        
        for tax in tax_rates:
            # Fetch the full tax account name including the company abbreviation
            account = frappe.get_list("Account", filters={
                "account_name": tax['tax_type'],
                "company": company_name
            }, fields=["name"])

            if not account:
                raise ValueError(f"Account '{tax['tax_type']}' not found for company '{company_name}'")
            
            # Add tax rates to the Item Tax Template
            item_tax_template.append("taxes", {
                "tax_type": account[0]['name'],
                "tax_rate": tax['rate']
            })
        
        # Save the new Item Tax Template
        item_tax_template.insert()
        frappe.db.commit()
        print(f"Item Tax Template '{template_name}' created successfully.")

    except Exception as e:
        print(f"Error creating Item Tax Template: {str(e)}")




def create_ksa_vat_settings():
    try:
        companies = frappe.get_all("Company", fields=["name"])
        print("Fetching companies...")

        for company in companies:
            company_name = company['name']
            print(f"Processing company: {company_name}")

            existing_ksa_vat_setting = frappe.get_all("KSA VAT Setting", filters={"company": company_name}, fields=["name"])

            if existing_ksa_vat_setting:
                print(f"Updating KSA VAT Setting for company: {company_name}")
                ksa_vat_setting = frappe.get_doc("KSA VAT Setting", existing_ksa_vat_setting[0]['name'])
            else:
                print(f"Creating KSA VAT Setting for company: {company_name}")
                ksa_vat_setting = frappe.get_doc({
                    "doctype": "KSA VAT Setting",
                    "company": company_name,
                    "ksa_vat_sales_accounts": [],
                    "ksa_vat_purchase_accounts": []
                })

            # Adding or updating sales and purchase settings
            for template in frappe.get_all("Item Tax Template", fields=["name"]):
                template_name = template['name']
                template_doc = frappe.get_doc("Item Tax Template", template_name)
                print(f"Processing template: {template_name}")

                for tax in template_doc.taxes:
                    if tax.tax_type:
                        # Check if accounts already exist
                        existing_sales_account = any(account.account == tax.tax_type for account in ksa_vat_setting.ksa_vat_sales_accounts)
                        existing_purchase_account = any(account.account == tax.tax_type for account in ksa_vat_setting.ksa_vat_purchase_accounts)

                        if not existing_sales_account:
                            ksa_vat_setting.append("ksa_vat_sales_accounts", {
                                "title": template_name,
                                "item_tax_template": template_name,
                                "account": tax.tax_type
                            })

                        if not existing_purchase_account:
                            ksa_vat_setting.append("ksa_vat_purchase_accounts", {
                                "title": template_name,
                                "item_tax_template": template_name,
                                "account": tax.tax_type
                            })

            ksa_vat_setting.save()
            frappe.db.commit()
            print(f"KSA VAT Setting for company '{company_name}' has been processed successfully.")
    except Exception as e:
        print(f"Error creating KSA VAT Setting: {str(e)}")



def ExecuteSales():
    # Check if the Selling Settings doctype exists
    if frappe.get_all('DocType', filters={'name': 'Selling Settings'}):
        # Check if the field already exists
        if not frappe.get_all('Custom Field', filters={'dt': 'Selling Settings', 'fieldname': 'default_tax_template'}):
            # Add the new field
            frappe.get_doc({
                'doctype': 'Custom Field',
                'dt': 'Selling Settings',
                'fieldname': 'default_tax_template',
                'label': 'Default Tax Template',
                'fieldtype': 'Link',
                'options': 'Item Tax Template',
                'insert_after': 'some_existing_field',  # Change this to the field after which you want to insert the new field
                'reqd': 0
            }).insert()
            frappe.db.commit()
        else:
            print(_("Field 'default_tax_template' already exists in 'Selling Settings'."))

    else:
        frappe.throw(_("The DocType 'Selling Settings' does not exist."))

def ExecuteBuy():
    # Check if the Selling Settings doctype exists
    if frappe.get_all('DocType', filters={'name': 'Buying Settings'}):
        # Check if the field already exists
        if not frappe.get_all('Custom Field', filters={'dt': 'Buying Settings', 'fieldname': 'default_tax_template'}):
            # Add the new field
            frappe.get_doc({
                'doctype': 'Custom Field',
                'dt': 'Buying Settings',
                'fieldname': 'default_tax_template',
                'label': 'Default Tax Template',
                'fieldtype': 'Link',
                'options': 'Item Tax Template',
                'insert_after': 'some_existing_field',  # Change this to the field after which you want to insert the new field
                'reqd': 0
            }).insert()
            frappe.db.commit()
        else:
            print(_("Field 'default_tax_template' already exists in 'Buying Settings'."))

    else:
        frappe.throw(_("The DocType 'Buying Settings' does not exist."))



# استدعاء الدالة عند الحاجة

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
