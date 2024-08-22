import frappe
from frappe import _

def execute(filters=None):
    columns, data = [], []

    # Define columns
    columns = [
        {"label": _("Customer ID"), "fieldname": "customer", "fieldtype": "Link", "options": "Customer", "width": 150},
        {"label": _("Customer Name"), "fieldname": "customer_name", "fieldtype": "Data", "width": 150},
        {"label": _("Customer PO Number"), "fieldname": "po_no", "fieldtype": "Data", "width": 150},
        {"label": _("SO Number"), "fieldname": "so_number", "fieldtype": "Link", "options": "Sales Order", "width": 150},
        {"label": _("Sales Invoice Number"), "fieldname": "sales_invoice_number", "fieldtype": "Link", "options": "Sales Invoice", "width": 150},
        {"label": _("Item Code"), "fieldname": "item_code", "fieldtype": "Data", "width": 150},
        {"label": _("Payment Status"), "fieldname": "payment_status", "fieldtype": "Data", "width": 150},
        {"label": _("Terminated Date"), "fieldname": "terminated_date", "fieldtype": "Date", "width": 150},
        {"label": _("Actual Start Date"), "fieldname": "actual_start_date", "fieldtype": "Date", "width": 150},
        {"label": _("End Date"), "fieldname": "end_date", "fieldtype": "Date", "width": 150},
        {"label": _("Duration"), "fieldname": "duration", "fieldtype": "Int", "width": 150},
        {"label": _("Type"), "fieldname": "custom_type", "fieldtype": "Data", "width": 150},
        {"label": _("Old Sales Order"), "fieldname": "custom_old_sales_order", "fieldtype": "Link", "options": "Sales Order", "width": 150},
        {"label": _("Status"), "fieldname": "status", "fieldtype": "Data", "width": 150},
        
    ]

    # Build conditions based on filters
    conditions = "WHERE so.docstatus = 1 AND so.custom_contacted = 0"
    
    if filters.get("customer"):
        conditions += " AND so.customer = %(customer)s"
    
    if filters.get("status"):
        conditions += """ AND (
            CASE
                WHEN sod.custom_terminate_date IS NOT NULL THEN 'Terminated'
                WHEN sod.custom_end_date < CURDATE() THEN 'Expired'
                WHEN sod.custom_end_date >= CURDATE() THEN 'Active'
                ELSE so.status
            END = %(status)s
        )"""
    
    if filters.get("po_no"):
        conditions += " AND so.po_no = %(po_no)s"
    
    if filters.get("item_code"):
        conditions += " AND sod.item_code = %(item_code)s"

    
    if filters.get("from_date"):
        conditions += " AND so.transaction_date >= %(from_date)s"
    
    if filters.get("to_date"):
        conditions += " AND so.transaction_date <= %(to_date)s"


    # Main query
    query = f"""
        SELECT 
            0 AS select_checkbox,  -- Default unchecked checkbox
            so.customer AS customer,
            so.customer_name AS customer_name, 
            so.po_no AS po_no, 
            so.name AS so_number, 
            si.name AS sales_invoice_number, 
            sod.item_code AS item_code, 
            sod.custom_terminate_date AS terminated_date, 
            CASE
                WHEN si.name IS NOT NULL THEN sii.custom_actual_start_date
                ELSE sod.custom_start_date
            END AS actual_start_date,
            CASE
                WHEN si.name IS NOT NULL THEN sii.custom_end_date
                ELSE sod.custom_end_date
            END AS end_date,
            sod.custom_duration AS duration, 
            so.custom_type AS custom_type,
            so.custom_old_sales_order AS custom_old_sales_order,
            CASE
                WHEN sod.custom_terminate_date IS NOT NULL THEN 'Terminated'
                WHEN sod.custom_end_date < CURDATE() THEN 'Expired'
                WHEN sod.custom_end_date >= CURDATE() THEN 'Active'
                ELSE so.status
            END AS status,
            CASE
                WHEN si.status = 'Paid' THEN 'Paid'
                WHEN si.status = 'Partially Paid' THEN 'Partially Paid'
                WHEN si.status = 'Return' THEN 'Return'
                ELSE 'Unpaid'
            END AS payment_status
        FROM 
            `tabSales Order` so
        LEFT JOIN 
            `tabSales Order Item` sod ON so.name = sod.parent
        LEFT JOIN `tabSales Invoice Item` sii ON so.name = sii.sales_order
        LEFT JOIN 
            `tabSales Invoice` si ON sii.parent = si.name AND si.docstatus = 1
        {conditions}
        ORDER BY 
            so.transaction_date DESC
    """

    # Fetching data
    data = frappe.db.sql(query, filters, as_dict=1)

    
    
    return columns, data




@frappe.whitelist()
def update_custom_contacted(sales_order_names):
    sales_order_names = frappe.parse_json(sales_order_names)
    for so_name in sales_order_names:
        frappe.db.set_value("Sales Order", so_name, "custom_contacted", 1)
        frappe.db.commit()
    return {"status": "success", "message": "Updated successfully"}
