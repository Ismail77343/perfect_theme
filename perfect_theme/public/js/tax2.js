// perfect_theme/public/js/sales_invoice_custom.js

frappe.ui.form.on('Sales Invoice', {
    onload: function(frm) {
        if (frm.is_new()) {
            // التحقق من إعدادات البيع للحصول على قالب الضريبة الافتراضي
            frappe.call({
                method: 'frappe.client.get_value',
                args: {
                    'doctype': 'Selling Settings',
                    'fieldname': 'default_tax_template'
                },
                callback: function(response) {
                    if (response.message && response.message.default_tax_template) {
                        const tax_template = response.message.default_tax_template;
                        
                        // الحصول على تفاصيل الضرائب من الـ Item Tax Template
                        frappe.call({
                            method: 'frappe.client.get',
                            args: {
                                'doctype': 'Item Tax Template',
                                'name': tax_template
                            },
                            callback: function(tax_response) {
                                if (tax_response.message) {
                                    let taxes = tax_response.message.taxes || [];
                                    taxes.forEach(function(tax) {
                                        frm.add_child('taxes', {
                                            'charge_type': 'On Net Total',
                                            'account_head': tax.tax_type,
                                            'rate': tax.tax_rate
                                        });
                                    });
                                    frm.refresh_field('taxes');
                                }
                            }
                        });
                    }
                }
            });
        }
    }
});

frappe.ui.form.on('Purchase Invoice', {
    onload: function(frm) {
        if (frm.is_new()) {
            // التحقق من إعدادات البيع للحصول على قالب الضريبة الافتراضي
            frappe.call({
                method: 'frappe.client.get_value',
                args: {
                    'doctype': 'Buying Settings',
                    'fieldname': 'default_tax_template'
                },
                callback: function(response) {
                    if (response.message && response.message.default_tax_template) {
                        const tax_template = response.message.default_tax_template;
                        
                        // الحصول على تفاصيل الضرائب من الـ Item Tax Template
                        frappe.call({
                            method: 'frappe.client.get',
                            args: {
                                'doctype': 'Item Tax Template',
                                'name': tax_template
                            },
                            callback: function(tax_response) {
                                if (tax_response.message) {
                                    let taxes = tax_response.message.taxes || [];
                                    taxes.forEach(function(tax) {
                                        frm.add_child('taxes', {
                                            'charge_type': 'On Net Total',
                                            'account_head': tax.tax_type,
                                            'rate': tax.tax_rate
                                        });
                                    });
                                    frm.refresh_field('taxes');
                                }
                            }
                        });
                    }
                }
            });
        }
    }
});
