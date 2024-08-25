

import frappe

def delete_workspace():
    try:
        # البحث عن الـ Workspace حسب الاسم
        workspace = frappe.get_doc("Workspace", {"label": "ERPNext Integrations"})
        if workspace:
            # حذف الـ Workspace
            workspace.delete()
            frappe.db.commit()
            print("Workspace 'ERPNext Integrations' deleted successfully.")
        else:
            print("Workspace 'ERPNext Integrations' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

def modify_workspaces():
    try:
        # البحث عن الـ Workspace المراد حذفه
        workspace_to_delete = frappe.db.get_value("Workspace", {"label": "ERPNext Integrations"}, "name")
        if workspace_to_delete:
            frappe.delete_doc("Workspace", workspace_to_delete)
            print("Workspace 'ERPNext Integrations' deleted successfully.")
        else:
            print("Workspace 'ERPNext Integrations' not found.")



    except Exception as e:
        print(f"An error occurred: {e}")
    
    try:
        # البحث عن الـ Workspace المراد إعادة تسميته
        workspace_to_rename = frappe.db.get_value("Workspace", {"name": "ERPNext Settings"}, "name")
        if workspace_to_rename:
            workspace_doc = frappe.get_doc("Workspace", workspace_to_rename)
            workspace_doc.label = "ErpAlfras Settings"
            workspace_doc.title = "ErpAlfras Settings"
            
            # تغيير الاسم لتجنب مشكلة "Page not found"
            new_name = "ErpAlfras-settings"
            frappe.rename_doc("Workspace", workspace_to_rename, new_name, force=True)
  
            workspace_doc.save()
            frappe.db.commit()
            print("Workspace 'ERPNext Settings' renamed to 'ErpAlfras Settings' successfully.")
        else:
            print("Workspace 'ERPNext Settings' not found.")
    
    except Exception as e:
        print(f"An error occurred: {e}")
def rename_workspace():
    # الوصول إلى قاعدة البيانات
    try:
        workspace = frappe.get_doc("Workspace", {"label": "ERPNext Settings"})
        if workspace:
            # تغيير الاسم
            workspace.label = "Erpalfras Settings"
            workspace.title = "Erpalfras Settings"
            workspace.save()
            frappe.db.commit()
            print("Workspace renamed successfully.")
        else:
            print("Workspace with label 'ERPNext Settings' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # تشغيل السكربت
    rename_workspace()
