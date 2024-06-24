// Copyright (c) 2022, Crisco Consulting and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Sales Pipeline Summary"] = {
	"filters": [
		{
			fieldname:"from_date",
			label: __("From Date"),
			fieldtype: "Date",
			default: frappe.datetime.add_months(frappe.datetime.month_start(), -1)

		},
		{
			fieldname:"to_date",
			label: __("To Date"),
			fieldtype: "Date",
			default: frappe.datetime.add_days(frappe.datetime.month_start(),-1)

		},
	]
};
