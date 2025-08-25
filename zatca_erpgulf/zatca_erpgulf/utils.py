from erpnext import get_default_company
import frappe
from frappe.utils.data import get_datetime
from zatca_erpgulf.zatca_erpgulf.sign_invoice import resubmit_invoices, zatca_call


@frappe.whitelist()
def invoices_reports(from_date, to_date):
    fdate = get_datetime(from_date)
    tdate = get_datetime(to_date)

    failed_invoices = frappe.get_all(
        "Sales Invoice",
        fields=["name", "custom_zatca_status", "custom_zatca_full_response"],
        filters=[
            ["posting_date", "between", [fdate, tdate]],
            ["custom_zatca_full_response", "like", "%ERROR%"],
            [
                "custom_zatca_status",
                "in",
                ["Not Submitted", "503 Service Unavailable"],
            ],
        ],
    )

    reported_invoices = frappe.get_all(
        "Sales Invoice",
        fields=["name", "custom_zatca_status", "custom_zatca_full_response"],
        filters=[
            ["posting_date", "between", [fdate, tdate]],
            ["custom_zatca_status", "=", "REPORTED"],
        ],
    )

    cleared_invoices = frappe.get_all(
        "Sales Invoice",
        fields=["name", "custom_zatca_status", "custom_zatca_full_response"],
        filters=[
            ["posting_date", "between", [fdate, tdate]],
            ["custom_zatca_status", "=", "CLEARED"],
        ],
    )
    return {
        "failed_invoices": failed_invoices,
        "reported_invoices": reported_invoices,
        "cleared_invoices": cleared_invoices,
    }


@frappe.whitelist()
def resubmit_zatca_invoices():
    failed_invoices = frappe.get_all(
        "Sales Invoice",
        filters=[
            ["custom_zatca_full_response", "like", "%ERROR%"],
            [
                "custom_zatca_status",
                "in",
                ["Not Submitted", "503 Service Unavailable"],
            ],
        ],
        pluck="name",
    )
    resubmit_invoices(failed_invoices)
