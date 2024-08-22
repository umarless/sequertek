frappe.query_reports["Sales Report"] = {
    "filters": [
        {
            "fieldname": "customer",
            "label": __("Customer ID"),
            "fieldtype": "Link",
            "options": "Customer",
            "default": "",
            "reqd": 0
        },
        {
            "fieldname": "status",
            "label": __("Status"),
            "fieldtype": "Select",
            "options": [
                "",
                "Terminated",
                "Expired",
                "Active"
            ],
            "default": "",
            "reqd": 0
        },
        {
            "fieldname": "po_no",
            "label": __("PO Number"),
            "fieldtype": "Data",
            "default": "",
            "reqd": 0
        },
        {
            "fieldname": "item_code",
            "label": __("Item Code"),
            "fieldtype": "Link",
            "options": "Item",
            "default": "",
            "reqd": 0
        }
    ],

    "onload": function(report) {
        report.page.add_inner_button(__('Remove Record'), function() {
            updateCustomContactedField();
        });
    },

    "get_datatable_options": function(options) {
        options.columns.unshift({
            id: 'select_checkbox',
            name: 'Select',
            width: 30,
            editable: false,
            format: value => {
                return `<input type="checkbox" class="select-row" data-select="${value}" />`;
            }
        });
        return options;
    }
};

// Function to update custom_contacted field via a whitelisted method
function updateCustomContactedField() {
    let selectedOrders = [];
    
    // Collect all selected Sales Orders
    $('.select-row:checked').each(function() {
        let $row = $(this).closest('.dt-row');
        let so_number = $row.find('.dt-cell[data-col-index="5"] .dt-cell__content').attr('title') || "";
        if (so_number) {
            selectedOrders.push(so_number);
        }
    });

    if (selectedOrders.length > 0) {
        frappe.call({
            method: "sequertek.sequertek.report.sales_report.sales_report.update_custom_contacted",  // Adjust the path if necessary
            args: {
                sales_order_names: JSON.stringify(selectedOrders)
            },
            callback: function(response) {
                if (!response.exc && response.message.status === "success") {
                    frappe.msgprint(__('Custom Contacted field updated successfully for selected records.'));
                    frappe.query_report.refresh();
                } else {
                    frappe.msgprint(__('There was an issue updating the records.'));
                }
            }
        });
    } else {
        frappe.msgprint(__('Please select at least one record to update.'));
    }
}
