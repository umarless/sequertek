# Copyright (c) 2022, Crisco Consulting and contributors
# For license information, please see license.txt

import frappe
from frappe import _

def execute(filters=None):
    filters = frappe._dict(filters or {})
    columns, data = [], []
    data, summary_data = get_data(filters)
    report_summary = get_report_summary(summary_data)
    columns = get_columns()
    return columns, data, None, None, report_summary

def get_conditions(filters):
    conditions = ''
    print(filters)
    if filters.get("from_date"):
        conditions += " and `tabOpportunity`.transaction_date>=%(from_date)s "
    if filters.get("to_date"):
        conditions += " and `tabOpportunity`.transaction_date<=%(to_date)s "
    if filters.get("user"):
        conditions += " and `tabOpportunity`.converted_by<=%(user)s "
    return conditions

def get_data(filters):
    conditions = get_conditions(filters)
    result = frappe.db.sql("""
                            SELECT
                                `tabOpportunity`.opportunity_from,
                                `tabOpportunity`.party_name,
                                `tabOpportunity`.customer_name,
                                `tabOpportunity`.transaction_date,
                                `tabOpportunity`.source,
                                `tabOpportunity`.next_step,
                                `tabOpportunity`.opportunity_type,
                                `tabOpportunity`.status,
                                `tabOpportunity`.converted_by,
                                `tabOpportunity`.sales_stage,
                                `tabOpportunity`.expected_closing,
                                `tabOpportunity`.type,
                                `tabOpportunity`.incumbent_partner,
                                `tabOpportunity`.contact_by,
                                `tabOpportunity`.contact_date,
                                `tabOpportunity`.to_discuss,
                                `tabOpportunity`.currency,
                                `tabOpportunity`.opportunity_amount,
                                `tabOpportunity`.probability,
                                `tabOpportunity`.territory,
                                `tabOpportunity`.campaign
                            FROM
                                `tabOpportunity`
                            WHERE
                                `tabOpportunity`.status != 'Closed'
                            AND
                                `tabOpportunity`.status != 'Lost'
                                {0}
                        """.format(conditions),filters,as_dict=1)
    summary_data=frappe.db.sql("""select
                        count(*) as count ,sales_stage
                    from `tabOpportunity`
                    WHERE
                            `tabOpportunity`.status != 'Closed'
                        AND
                            `tabOpportunity`.status != 'Lost'
                            {0}
                    Group by `tabOpportunity`.sales_stage
                    """.format(conditions),filters,as_dict=1)
    return result, summary_data

def get_report_summary(summary_data):
    summary = []
    for sales_stage in summary_data:
        summary.append(
            {"value": sales_stage['count'], "label": sales_stage['sales_stage'], "datatype": "Data"},
        )
    return summary

def get_columns():
    return [
        {
            "fieldname": "opportunity_from",
            "label": _("Opportunity From"),
            "fieldtype": "Data",
            "width": 100,
        },
        {
            "fieldname": "party_name",
            "label": _("Party Name"),
            "fieldtype": "Data",
            "width": 200,
        },
        {
            "fieldname": "customer_name",
            "label": _("Customer Name"),
            "fieldtype": "Data",
            "width": 300,
        },
        {
            "fieldname": "transaction_date",
            "label": _("Date"),
            "fieldtype": "Date",
            "width": 150,
        },
        {
            "fieldname": "source",
            "label": _("Source"),
            "fieldtype": "Data",
            "width": 200,
        },
        {
            "fieldname": "opportunity_type",
            "label": _("Type"),
            "fieldtype": "Data",
            "width": 100,
        },
        {
            "fieldname": "status",
            "label": _("Status"),
            "fieldtype": "Data",
            "width": 100,
        },
        {
            "fieldname": "converted_by",
            "label": _("Converted By"),
            "fieldtype": "Link",
            "options":"User",
            "width": 130,
        },
        {
            "fieldname": "sales_stage",
            "label": _("Sales Stage"),
            "fieldtype": "Data",
            "width": 130,
        },
        {
            "fieldname": "expected_closing",
            "label": _("Expected Closing"),
            "fieldtype": "Data",
            "width": 150,
        },
        {
            "fieldname": "type",
            "label": _("Type"),
            "fieldtype": "Data",
            "width": 110,
        },
        {
            "fieldname": "incumbent_partner",
            "label": _("Incumbent Partner"),
            "fieldtype": "Data",
            "width": 140,
        },
        {
            "fieldname": "contact_by",
            "label": _("Contact By"),
            "fieldtype": "Link",
            "options": "User",
            "width": 130,
        },
        {
            "fieldname": "contact_date",
            "label": _("Contact Date"),
            "fieldtype": "Date",
            "width": 150,
        },
        {
            "fieldname": "to_discuss",
            "label": _("To Discuss"),
            "fieldtype": "Date",
            "width": 150,
        },
        {
            "fieldname": "currency",
            "label": _("Currency"),
            "fieldtype": "Data",
            "width": 70,
        },
        {
            "fieldname": "opportunity_amount",
            "label": _("Opp. Amount"),
            "fieldtype": "Currency",
            "width": 120,
        },
        {
            "fieldname": "probability",
            "label": _("Probability"),
            "fieldtype": "Percent",
            "width": 70,
        },
        {
            "fieldname": "territory",
            "label": _("Territory"),
            "fieldtype": "Data",
            "width": 120,
        },
        {
            "fieldname": "campaign",
            "label": _("Campaign"),
            "fieldtype": "Data",
            "width": 190,
        }
    ]
