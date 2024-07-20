from . import __version__ as app_version

app_name = "perfect_theme"
app_title = "perfect_theme"
app_publisher = "ismail"
app_description = "perfect_theme"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "himiismail123@gmail.com"
app_license = "MIT"
app_logo_url = "/assets/perfect_theme/images/theme-favicon.svg"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
#   app_include_css = "/assets/perfect_theme/css/StyleDesk123.css"
app_include_css = "/assets/perfect_theme/css/StyleDesk4.css"
app_include_js = ["/assets/perfect_theme/js/perfect_theme10.js"]

# include js, css files in header of web template
web_include_css = "/assets/perfect_theme/css/perfect_theme3.css"
web_include_js = "/assets/perfect_theme/js/theme_footer.js"

website_context = {
    "favicon": "/assets/perfect_theme/images/theme-favicon.svg",
	"splash_image": "/assets/perfect_theme/images/theme-logo.png"
}
override_whitelisted_methods = {
    'perfect_theme.api.get_items': 'perfect_theme.api.get_items'
}
# website_context = {
#     "header_html": "includes/perfect_theme_header"
# }
# def extend_website_routes(context):
#     context.update({
#         "website_context": "perfect_theme"
#     })

# base_template = "perfect_theme/templates/base.html"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "perfect_theme/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "perfect_theme.install.before_install"
# apps/perfect_theme/perfect_theme/hooks.py

# تضمين دوال التثبيت وإلغاء التثبيت
# after_install = "perfect_theme.install.after_install"
# before_uninstall = "perfect_theme.install.before_uninstall"

# Uninstallation
# ------------

# before_uninstall = "perfect_theme.uninstall.before_uninstall"
# after_uninstall = "perfect_theme.uninstall.after_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "perfect_theme.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
#	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
#	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
#	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
#	"*": {
#		"on_update": "method",
#		"on_cancel": "method",
#		"on_trash": "method"
#	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
#	"all": [
#		"perfect_theme.tasks.all"
#	],
#	"daily": [
#		"perfect_theme.tasks.daily"
#	],
#	"hourly": [
#		"perfect_theme.tasks.hourly"
#	],
#	"weekly": [
#		"perfect_theme.tasks.weekly"
#	]
#	"monthly": [
#		"perfect_theme.tasks.monthly"
#	]
# }

# Testing
# -------

# before_tests = "perfect_theme.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
#	"frappe.desk.doctype.event.event.get_events": "perfect_theme.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
#	"Task": "perfect_theme.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Request Events
# ----------------
# before_request = ["perfect_theme.utils.before_request"]
# after_request = ["perfect_theme.utils.after_request"]

# Job Events
# ----------
# before_job = ["perfect_theme.utils.before_job"]
# after_job = ["perfect_theme.utils.after_job"]

# User Data Protection
# --------------------

user_data_fields = [
	{
		"doctype": "{doctype_1}",
		"filter_by": "{filter_by}",
		"redact_fields": ["{field_1}", "{field_2}"],
		"partial": 1,
	},
	{
		"doctype": "{doctype_2}",
		"filter_by": "{filter_by}",
		"partial": 1,
	},
	{
		"doctype": "{doctype_3}",
		"strict": False,
	},
	{
		"doctype": "{doctype_4}"
	}
]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
#	"perfect_theme.auth.validate"
# ]

