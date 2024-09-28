import frappe;
from frappe import _
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields
from frappe.custom.doctype.custom_field.custom_field import create_custom_field













def add_sales_setting():
    # تحقق مما إذا كان الحقل موجودًا بالفعل لتجنب التكرار
    if not frappe.db.exists('Custom Field', 'Selling Settings-create_delivery_note_on_submit'):
        create_custom_field('Selling Settings', {
            'fieldname': 'create_delivery_note_on_submit',
            'fieldtype': 'Check',
            'label': 'Create Delivery Note on Submit',
            'insert_after': 'some_field_name',  # استبدل "some_field_name" باسم الحقل المناسب
            'reqd': 0
        })
def after_install():
    add_sales_setting()
    make_custom_fields()
    create_accounts()
    create_item_tax_templates()
    create_ksa_vat_settings()
    # ExecuteSales()
    # ExecuteBuy()
    # execute()
    add_tax_settings_to_workspace()



def make_custom_fields():

	is_zero_rated = dict(
		fieldname="is_zero_rated",
		label="Is Zero Rated",
		fieldtype="Check",
		fetch_from="item_code.is_zero_rated",
		insert_after="description",
		print_hide=1,
	)

	is_exempt = dict(
		fieldname="is_exempt",
		label="Is Exempt",
		fieldtype="Check",
		fetch_from="item_code.is_exempt",
		insert_after="is_zero_rated",
		print_hide=1,
	)

	purchase_invoice_fields = [
		dict(
			fieldname="company_trn",
			label="Company TRN",
			fieldtype="Read Only",
			insert_after="shipping_address",
			fetch_from="company.tax_id",
			print_hide=1,
		),
		dict(
			fieldname="supplier_name_in_arabic",
			label="Supplier Name in Arabic",
			fieldtype="Read Only",
			insert_after="supplier_name",
			fetch_from="supplier.supplier_name_in_arabic",
			print_hide=1,
		),
	]

	sales_invoice_fields = [
		dict(
			fieldname="company_trn",
			label="Company TRN",
			fieldtype="Read Only",
			insert_after="company_address",
			fetch_from="company.tax_id",
			print_hide=1,
		),
		dict(
			fieldname="customer_name_in_arabic",
			label="Customer Name in Arabic",
			fieldtype="Read Only",
			insert_after="customer_name",
			fetch_from="customer.customer_name_in_arabic",
			print_hide=1,
		),
		dict(
			fieldname="ksa_einv_qr",
			label="KSA E-Invoicing QR",
			fieldtype="Attach Image",
			read_only=1,
			no_copy=1,
			hidden=1,
		),
	]

	custom_fields = {
		"Item": [is_zero_rated, is_exempt],
		"Customer": [
			dict(
				fieldname="customer_name_in_arabic",
				label="Customer Name in Arabic",
				fieldtype="Data",
				insert_after="customer_name",
			),
		],
		"Supplier": [
			dict(
				fieldname="supplier_name_in_arabic",
				label="Supplier Name in Arabic",
				fieldtype="Data",
				insert_after="supplier_name",
			),
		],
		"Purchase Invoice": purchase_invoice_fields,
		"Purchase Order": purchase_invoice_fields,
		"Purchase Receipt": purchase_invoice_fields,
		"Sales Invoice": sales_invoice_fields,
		"POS Invoice": sales_invoice_fields,
		"Sales Order": sales_invoice_fields,
		"Delivery Note": sales_invoice_fields,
		"Sales Invoice Item": [is_zero_rated, is_exempt],
		"POS Invoice Item": [is_zero_rated, is_exempt],
		"Purchase Invoice Item": [is_zero_rated, is_exempt],
		"Sales Order Item": [is_zero_rated, is_exempt],
		"Delivery Note Item": [is_zero_rated, is_exempt],
		"Quotation Item": [is_zero_rated, is_exempt],
		"Purchase Order Item": [is_zero_rated, is_exempt],
		"Purchase Receipt Item": [is_zero_rated, is_exempt],
		"Supplier Quotation Item": [is_zero_rated, is_exempt],
		"Address": [
			dict(
				fieldname="address_in_arabic",
				label="Address in Arabic",
				fieldtype="Data",
				insert_after="address_line2",
			)
		],
		"Company": [
			dict(
				fieldname="company_name_in_arabic",
				label="Company Name In Arabic",
				fieldtype="Data",
				insert_after="company_name",
			)
		],
	}

	create_custom_fields(custom_fields, ignore_validate=True, update=True)



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





def add_tax_settings_to_workspace():
    # تحقق مما إذا كان workspace لـ Erpalfras Settings موجودًا
    workspace_name = "Erpalfras Settings"
    workspace = frappe.get_doc("Workspace", workspace_name)

    if workspace:
        # تحقق مما إذا كان System Settings موجودًا في الـ workspace
        system_settings_section = None
        for link in workspace.links:
            if link.label == "System Settings" and link.type == "Link":
                system_settings_section = link
                break

        # إذا كانت System Settings موجودة
        if system_settings_section:
            # تحقق مما إذا كانت Tax Settings موجودة بالفعل
            tax_settings_exists = False
            for link in workspace.links:
                if link.label == "Tax Settings" and link.parent_label == "System Settings":
                    tax_settings_exists = True
                    break

            if not tax_settings_exists:
                # إضافة Tax Settings تحت System Settings
                workspace.append("links", {
                    "type": "Link",
                    "label": "Tax Settings",
                    "link_type": "DocType",
                    "link_to": "Tax Settings",
                    "parent_label": "System Settings",
                    "is_query_report": False
                })
                workspace.save()
                frappe.msgprint("Tax Settings تم إضافتها بنجاح تحت System Settings")
            else:
                frappe.msgprint("Tax Settings موجودة بالفعل تحت System Settings")
        else:
            frappe.msgprint("System Settings غير موجودة في Erpalfras Settings")
    else:
        frappe.msgprint(f"الـ workspace {workspace_name} غير موجود")

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
