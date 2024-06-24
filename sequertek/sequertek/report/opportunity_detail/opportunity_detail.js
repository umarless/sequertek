// Copyright (c) 2022, Crisco Consulting and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Opportunity Detail"] = {
	"filters": [
        {
            "fieldname":"from_date",
            "label": __("From Date"),
            "fieldtype": "Date",
            "width": "80",
            "default": frappe.datetime.add_months(frappe.datetime.get_today(), -1),
        },
        {
            "fieldname":"to_date",
            "label": __("To Date"),
            "fieldtype": "Date",
            "width": "80",
            "default": frappe.datetime.get_today()
        },
        {
            "fieldname":"user",
            "label": __("User"),
            "fieldtype": "Link",
            "options": 'User'
        },
	]
};
