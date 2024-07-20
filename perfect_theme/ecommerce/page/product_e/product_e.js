frappe.pages['product_e'].on_page_load = function(wrapper) {
	var page = frappe.ui.make_app_page({
		parent: wrapper,
		title: 'Products',
		single_column: true
	});
}