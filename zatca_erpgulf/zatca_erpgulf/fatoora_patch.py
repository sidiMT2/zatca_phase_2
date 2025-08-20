from math import e
from erpnext import get_default_company
import frappe


def execute():
    try:

        print("Started Fatoora Pathch")

        company = frappe.get_doc("Company", get_default_company())
        tax_templates = frappe.get_all(
            "Item Tax Template",
            filters=[
                [
                    "name",
                    "in",
                    [
                        f"KSA VAT 15% - {company.abbr}",
                        f"KSA VAT Exempted - {company.abbr}",
                    ],
                ]
            ],
        )
        for template in tax_templates:
            doc = frappe.get_doc("Item Tax Template", template)
            tax_rate = doc.taxes and doc.taxes[0].get("tax_rate")
            if tax_rate is not None and tax_rate == 0:
                doc.custom_zatca_tax_category = "Zero Rated"
                doc.custom_exemption_reason_code = "VATEX-SA-35"

            elif tax_rate and int(tax_rate) == 15:
                doc.custom_zatca_tax_category = "Standard"
            doc.save(ignore_permissions=True)
        print("Ended Fatoora Pach")
    except e:
        print(e)
