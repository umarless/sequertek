frappe.ui.form.on("Employee Onboarding", {
    refresh: function (frm) {
        // Ensure the buttons are added only if the document is submitted
        if (frm.doc.docstatus === 1) {
            // Add the "User" button
            frm.add_custom_button(
                __("User"),
                function () {
                    // Call the server-side function to create a User
                    frappe.call({
                        method: "sequertek.sequertek.override_function.create.create_user_from_onboarding",
                        args: {
                            employee_onboarding_name: frm.doc.name
                        },
                        callback: function(response) {
                            if (response.message) {
                                frappe.msgprint(response.message);
                            }
                        }
                    });
                },
                __("Create")
            );

            // Override the "Employee" button when employee is present
            if (frm.doc.employee) {
                frm.add_custom_button(
                    __("Employee"),
                    function () {
                        // Add your custom functionality here
                        frappe.set_route("Form", "Employee", frm.doc.employee);
                    },
                    __("View")
                );
            }

            // Override the "Create Employee" button when no employee is present and docstatus is 1
            if (!frm.doc.employee && frm.doc.docstatus === 1) {
                frm.add_custom_button(
                    __("Employee  "),
                    function () {
                        // Add your custom functionality here
                        frappe.model.open_mapped_doc({
                            method: "sequertek.sequertek.override_function.create.make_employee",
                            frm: frm,
                        });
                    },
                    __("Create")
                );
                frm.page.set_inner_btn_group_as_primary(__("Create"));
            }
        }
    },
});
