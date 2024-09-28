import frappe

def on_submit_sales_invoice(doc, method):
    # الحصول على إعدادات المبيعات
    sales_settings = frappe.get_single('Selling Settings')
    
    # التحقق مما إذا كان يجب إنشاء مذكرة استلام
    if sales_settings.create_delivery_note_on_submit:
        try:
            # إنشاء مذكرة استلام جديدة
            delivery_note = frappe.get_doc({
                "doctype": "Delivery Note",
                "customer": doc.customer,
                "items": []
            })

            # إضافة العناصر من فاتورة البيع إلى مذكرة الاستلام
            for item in doc.items:
                delivery_note.append('items', {
                    "item_code": item.item_code,
                    "qty": item.qty,
                    "rate": item.rate,
                    # أضف المزيد من الحقول حسب الحاجة
                })

            # حفظ ومتابعة مذكرة الاستلام
            delivery_note.insert()
            delivery_note.submit()

            # ربط مذكرة الاستلام بالفاتورة
            doc.delivery_notes = [delivery_note.name]  # قم بتعديل هذا الحقل حسب الهيكل المناسب في فاتورة البيع
            doc.save()
        except Exception as e:
            frappe.throw(f"Error creating Delivery Note: {str(e)}")

