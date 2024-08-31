import frappe
from frappe.utils import flt

def execute(filters=None):
    columns, data = [], []
    
    if isinstance(filters, str):
        filters = frappe._dict(json.loads(filters))

    columns = get_columns()
    data = get_data(filters)
    
    return columns, data

def get_columns():
    return [
        {"label": "Company", "fieldname": "company", "fieldtype": "Link", "options": "Company", "width": 150},
        {"label": "Posting Date", "fieldname": "posting_date", "fieldtype": "Date", "width": 120},
        {"label": "Account", "fieldname": "account", "fieldtype": "Link", "options": "Account", "width": 180},
        {"label": "Debit", "fieldname": "debit", "fieldtype": "Currency", "width": 120},
        {"label": "Credit", "fieldname": "credit", "fieldtype": "Currency", "width": 120},
        {"label": "Voucher Type", "fieldname": "voucher_type", "fieldtype": "Data", "width": 150},
        {"label": "Voucher No", "fieldname": "voucher_no", "fieldtype": "Link", "options": "GL Entry", "width": 180},
        {"label": "Tax Amount", "fieldname": "tax_amount", "fieldtype": "Currency", "width": 120},
    ]

def get_data(filters):
    conditions = "1 = 1"
    if filters.get("company"):
        conditions += " and company = %(company)s"
    if filters.get("account"):
        conditions += " and account = %(account)s"
    if filters.get("from_date"):
        conditions += " and posting_date >= %(from_date)s"
    if filters.get("to_date"):
        conditions += " and posting_date <= %(to_date)s"

    entries = frappe.db.sql("""
        select 
            company, 
            posting_date, 
            account, 
            debit, 
            credit, 
            voucher_type, 
            voucher_no,
            case when debit > 0 then debit else credit end as tax_amount
        from 
            `tabGL Entry`
        where 
            {conditions}
    """.format(conditions=conditions), filters, as_dict=1)

    return entries
