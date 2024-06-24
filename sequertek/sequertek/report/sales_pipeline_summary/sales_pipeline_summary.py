# Copyright (c) 2022, Crisco Consulting and contributors
# For license information, please see license.txt

import frappe
from frappe import _

def execute(filters=None):
    columns, data = [], []
    columns = get_columns()
    data = get_result(filters)
    return columns, data

def get_columns():
    columns = [
        {
            "fieldname": "sales_person",
            "label": _("Sales Person"),
            "fieldtype": "Link",
            "options": "Employee",
            "width": 300,
        }
    ]
    col_heads = frappe.db.get_all("Sales Stage",pluck="name")
    for col in col_heads:
        columns.append(
            {
                "fieldname": frappe.scrub(col),
                "label": _(col),
                "fieldtype": "Data",
                "width": 100,
            }
        )
    return columns

def get_conditions(filters):
    conditions = ''


    if filters.get("from_date"):
        conditions += " and transaction_date >=%(from_date)s"

    if filters.get("to_date"):
        conditions += " and transaction_date <=%(to_date)s"

    return conditions


def get_data_v14(filters):
    conditions = get_conditions(filters)
    if filters.get("user"):
        conditions += " and opportunity_owner >=%(user)s"

    data = frappe.db.sql('''
                    SELECT
                        opportunity_owner,
                        sales_stage,
                        count(*) as count
                    FROM
                        `tabOpportunity`
                    WHERE
                        status != "Closed" {0}
                    Group By
                        opportunity_owner,
                        sales_stage
                  '''.format(conditions),filters,as_dict=1)
    return data

def get_data_v13(filters):
    conditions = get_conditions(filters)
    if filters.get("user"):
        conditions += " and converted_by >=%(user)s"
    data = frappe.db.sql('''
                    SELECT
                        converted_by as opportunity_owner,
                        sales_stage,
                        count(*) as count
                    FROM
                        `tabOpportunity`
                    WHERE
                        status != "Closed" {0}
                    Group By
                        opportunity_owner,
                        sales_stage
                  '''.format(conditions),filters,as_dict=1)
    return data

def get_result(filters):
    data = get_data_v13(filters)
    owners = set([row.opportunity_owner for row in data])
    result = []
    for owner in owners:
        row = {"sales_person":owner }
        for d in data:
            if d['opportunity_owner'] == owner:
                row.update({frappe.scrub(d.sales_stage):d.count})
        result.append(row)

    return result
