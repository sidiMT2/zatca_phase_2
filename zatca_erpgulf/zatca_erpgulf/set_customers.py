from math import e
from erpnext import get_default_company
import frappe


def execute():
    try:

        print("Started Customer Patch")
        customers = frappe.get_all("Customer", pluck="name")
        for customer in customers:
            frappe.db.set_value(
                "Customer", customer, "custom_b2c", 1, update_modified=False
            )
        frappe.db.commit()
        print("Ended Fatoora Pach")
    except e:
        print(e)
