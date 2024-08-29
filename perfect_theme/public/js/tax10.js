// perfect_theme/public/js/sales_invoice_custom.js

frappe.ui.form.on('Sales Invoice', {
    onload: function(frm) {
        if (frm.is_new()) {
            // تنفيذ الكود عند تغيير الشركة
            frm.fields_dict.company.$input.on('change', function() {
                let company = frm.doc.company;

                if (company) {
                    frm.clear_table('taxes');

                    // جلب إعدادات الضريبة
                    frappe.call({
                        method: 'frappe.client.get',
                        args: {
                            doctype: 'Tax Settings'
                        },
                        callback: function(response) {
                            if (response.message && response.message.sales) {
                                let sales_tax_templates = response.message.sales;

                                // البحث عن الشركة في الجدول الفرعي
                                let tax_template = null;
                                sales_tax_templates.forEach(function(row) {
                                    if (row.company === company) {
                                        tax_template = row.template_tax;
                                    }
                                });

                                // إذا تم العثور على قالب الضريبة
                                if (tax_template) {
                                    // جلب تفاصيل الضرائب من قالب الضريبة
                                    frappe.call({
                                        method: 'frappe.client.get',
                                        args: {
                                            doctype: 'Item Tax Template',
                                            name: tax_template
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
                        }
                    });
                }
            });
            let company = frm.doc.company;

                if (company) {
                    frm.clear_table('taxes');

                    // جلب إعدادات الضريبة
                    frappe.call({
                        method: 'frappe.client.get',
                        args: {
                            doctype: 'Tax Settings'
                        },
                        callback: function(response) {
                            if (response.message && response.message.sales) {
                                let sales_tax_templates = response.message.sales;

                                // البحث عن الشركة في الجدول الفرعي
                                let tax_template = null;
                                sales_tax_templates.forEach(function(row) {
                                    if (row.company === company) {
                                        tax_template = row.template_tax;
                                    }
                                });

                                // إذا تم العثور على قالب الضريبة
                                if (tax_template) {
                                    // جلب تفاصيل الضرائب من قالب الضريبة
                                    frappe.call({
                                        method: 'frappe.client.get',
                                        args: {
                                            doctype: 'Item Tax Template',
                                            name: tax_template
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
                        }
                    });
                }
        }
    }
});



frappe.ui.form.on('Purchase Invoice', {
    onload: function(frm) {
        if (frm.is_new()) {
            // تنفيذ الكود عند تغيير الشركة
            frm.fields_dict.company.$input.on('change', function() {
                let company = frm.doc.company;

                if (company) {
                    frm.clear_table('taxes');

                    // جلب إعدادات الضريبة
                    frappe.call({
                        method: 'frappe.client.get',
                        args: {
                            doctype: 'Tax Settings'
                        },
                        callback: function(response) {
                            if (response.message && response.message.buy_settings) {
                                let sales_tax_templates = response.message.buy_settings;

                                // البحث عن الشركة في الجدول الفرعي
                                let tax_template = null;
                                sales_tax_templates.forEach(function(row) {
                                    if (row.company === company) {
                                        tax_template = row.template_tax;
                                    }
                                });

                                // إذا تم العثور على قالب الضريبة
                                if (tax_template) {
                                    // جلب تفاصيل الضرائب من قالب الضريبة
                                    frappe.call({
                                        method: 'frappe.client.get',
                                        args: {
                                            doctype: 'Item Tax Template',
                                            name: tax_template
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
                        }
                    });
                }
            });
            let company = frm.doc.company;

                if (company) {
                    // جلب إعدادات الضريبة
                    frm.clear_table('taxes');

                    frappe.call({
                        method: 'frappe.client.get',
                        args: {
                            doctype: 'Tax Settings'
                        },
                        callback: function(response) {
                            if (response.message && response.message.buy_settings) {
                                let sales_tax_templates = response.message.buy_settings;

                                // البحث عن الشركة في الجدول الفرعي
                                let tax_template = null;
                                sales_tax_templates.forEach(function(row) {
                                    if (row.company === company) {
                                        tax_template = row.template_tax;
                                    }
                                });

                                // إذا تم العثور على قالب الضريبة
                                if (tax_template) {
                                    // جلب تفاصيل الضرائب من قالب الضريبة
                                    frappe.call({
                                        method: 'frappe.client.get',
                                        args: {
                                            doctype: 'Item Tax Template',
                                            name: tax_template
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
                        }
                    });
                }
        }
    }
});




