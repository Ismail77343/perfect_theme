import frappe
from frappe import enqueue

def after_save_company(doc, method):
    try:
        frappe.msgprint(f"Added {doc.name}")
        # افترض أن create_accounts هي دالة تقوم بإنشاء حسابات بناءً على المستند doc
        enqueue(create_accounts, doc.name, queue='long')
    except Exception as e:
        # تسجيل الخطأ في سجل الأخطاء
        frappe.log_error(f"Error in after_save_company for {doc.name}: {str(e)}", "Company Save Error")


def create_accounts(company_name):
    frappe.msgprint(f"Added {doc.name}")

    try:
        create_account("Excise 100%", company_name)
        create_account("Excise 50%", company_name)
        create_account("VAT 15%", company_name)
        create_account("VAT 5%", company_name)
        create_account("VAT Zero", company_name)
    except Exception as e:
        frappe.log_error(f"Error in create_accounts: {str(e)}", "Create Accounts Error")

def create_account(account_name, company_name):
    try:
        companies = frappe.get_all(
            "Company",
            filters={"name": company_name},
            fields=["name"]
        )
        
        for company in companies:
            company_name = company['name']
            
            parent_account = frappe.db.get_value("Account", {"account_type": "Tax", "is_group": 1, "company": company_name}, "name")
            
            if not parent_account:
                frappe.throw(f"No group account of type 'Tax' found in company {company_name}. Please create one first.")
            
            if not frappe.db.exists("Account", {"account_name": account_name, "company": company_name}):
                new_account = frappe.get_doc({
                    "doctype": "Account",
                    "account_name": account_name,
                    "parent_account": parent_account,
                    "company": company_name,
                    "is_group": 0,
                    "root_type": frappe.db.get_value("Account", parent_account, "root_type"),
                    "report_type": frappe.db.get_value("Account", parent_account, "report_type"),
                    "account_type": "Tax"
                })
                new_account.insert(ignore_permissions=True)
                frappe.msgprint(f"Account '{account_name}' has been added under '{parent_account}' in company '{company_name}'.")
            else:
                frappe.msgprint(f"Account '{account_name}' already exists in company '{company_name}'.")
    except Exception as e:
        frappe.log_error(f"Error in create_account for {company_name}: {str(e)}", "Create Account Error")

def create_item_tax_templates(company_name):
    try:
        companies = frappe.get_all(
            "Company",
            filters={"name": company_name},
            fields=["name"]
        )

        for company in companies:
            company_name = company['name']
            tax_rates = [
                {'tax_type': 'Excise 100%', 'rate': 100},
            ]
            create_item_tax_template("Excise 100%", tax_rates, company_name)
            
            tax_rates = [
                {'tax_type': 'Excise 50%', 'rate': 50},
            ]
            create_item_tax_template("Excise 50%", tax_rates, company_name)

            tax_rates = [
                {'tax_type': 'VAT 15%', 'rate': 15},
            ]
            create_item_tax_template("VAT 15%", tax_rates, company_name)

            tax_rates = [
                {'tax_type': 'VAT 5%', 'rate': 5},
            ]
            create_item_tax_template("VAT 5%", tax_rates, company_name)

            tax_rates = [
                {'tax_type': 'VAT Zero', 'rate': 0},
            ]
            create_item_tax_template("VAT Zero", tax_rates, company_name)
    except Exception as e:
        frappe.log_error(f"Error in create_item_tax_templates for {company_name}: {str(e)}", "Create Item Tax Templates Error")

def create_item_tax_template(template_name, tax_rates, company_name):
    try:
        item_tax_template = frappe.get_doc({
            "doctype": "Item Tax Template",
            "title": template_name,
            "taxes": []
        })
        
        for tax in tax_rates:
            account = frappe.get_list("Account", filters={
                "account_name": tax['tax_type'],
                "company": company_name
            }, fields=["name"])

            if not account:
                raise ValueError(f"Account '{tax['tax_type']}' not found for company '{company_name}'")
            
            item_tax_template.append("taxes", {
                "tax_type": account[0]['name'],
                "tax_rate": tax['rate']
            })
        
        item_tax_template.insert(ignore_permissions=True)
        frappe.msgprint(f"Item Tax Template '{template_name}' created for company '{company_name}'.")
    except Exception as e:
        frappe.log_error(f"Error in create_item_tax_template for {company_name}: {str(e)}", "Create Item Tax Template Error")