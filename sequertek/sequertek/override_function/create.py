import frappe
from frappe import _
from frappe.model.mapper import get_mapped_doc

from hrms.controllers.employee_boarding_controller import EmployeeBoardingController
@frappe.whitelist()
def create_user_from_onboarding(employee_onboarding_name):
    # Fetch the Employee Onboarding document
    onboarding_doc = frappe.get_doc("Employee Onboarding", employee_onboarding_name)

    # Use the email provided in the onboarding document
    email = onboarding_doc.email_id
    first_name = onboarding_doc.employee_name.split()[0]  
    last_name = " ".join(onboarding_doc.employee_name.split()[1:])  

    
    if not frappe.db.exists("User", email):
        new_user = frappe.get_doc({
            "doctype": "User",
            "email": email,
            "first_name": first_name,
            "last_name": last_name,
            "enabled": 1,
            "send_welcome_email": 1  # Send welcome email if needed
        })
        new_user.insert(ignore_permissions=True)
        frappe.msgprint(_("User {0} created successfully").format(email))
    else:
        frappe.msgprint(_("User {0} already exists").format(email))










class IncompleteTaskError(frappe.ValidationError):
	pass


class EmployeeOnboarding(EmployeeBoardingController):
	def validate(self):
		super().validate()
		self.set_employee()
		self.validate_duplicate_employee_onboarding()

	def set_employee(self):
		if not self.employee:
			self.employee = frappe.db.get_value("Employee", {"job_applicant": self.job_applicant}, "name")

	def validate_duplicate_employee_onboarding(self):
		emp_onboarding = frappe.db.exists(
			"Employee Onboarding", {"job_applicant": self.job_applicant, "docstatus": ("!=", 2)}
		)
		if emp_onboarding and emp_onboarding != self.name:
			frappe.throw(
				_("Employee Onboarding: {0} already exists for Job Applicant: {1}").format(
					frappe.bold(emp_onboarding), frappe.bold(self.job_applicant)
				)
			)

	def validate_employee_creation(self):
		if self.docstatus != 1:
			frappe.throw(_("Submit this to create the Employee record"))
		else:
			for activity in self.activities:
				if not activity.required_for_employee_creation:
					continue
				else:
					task_status = frappe.db.get_value("Task", activity.task, "status")
					if task_status not in ["Completed", "Cancelled"]:
						frappe.throw(
							_("All the mandatory tasks for employee creation are not completed yet."),
							IncompleteTaskError,
						)

	def on_submit(self):
		super().on_submit()

	def on_update_after_submit(self):
		self.create_task_and_notify_user()

	def on_cancel(self):
		super().on_cancel()

	@frappe.whitelist()
	def mark_onboarding_as_completed(self):
		for activity in self.activities:
			frappe.db.set_value("Task", activity.task, "status", "Completed")
		frappe.db.set_value("Project", self.project, "status", "Completed")
		self.boarding_status = "Completed"
		self.save()


@frappe.whitelist()
def make_employee(source_name, target_doc=None):
    
    # Fetch the Employee Onboarding document
    doc = frappe.get_doc("Employee Onboarding", source_name)
    
    # Check if the User exists based on the email ID
    if not frappe.db.exists("User", {"email": doc.email_id}):
        frappe.throw("Please Create User!!")
    
    # Validate if employee creation tasks are completed
    doc.validate_employee_creation()

    def set_missing_values(source, target):
        # Set personal email and status in the Employee record
        target.personal_email = frappe.db.get_value("Job Applicant", source.job_applicant, "email_id")
        target.status = "Active"
        
        # Map custom fields
        target.custom_pre_onboarding_template = source.custom_pre_onboarding_template
        target.custom_pre_onboarding_activities = source.custom_pre_onboarding_activities

    # Map fields from Employee Onboarding to Employee
    doc = get_mapped_doc(
        "Employee Onboarding",
        source_name,
        {
            "Employee Onboarding": {
                "doctype": "Employee",
                "field_map": {
                    "first_name": "employee_name",
                    "employee_grade": "grade",
                    # Add any other standard field mappings here
                },
                "field_no_map": ["custom_pre_onboarding_template", "custom_pre_onboarding_activities"]
            }
        },
        target_doc,
        set_missing_values,
    )
    return doc



